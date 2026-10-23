#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Child, Command};
use std::sync::{Arc, Mutex};
use std::time::Duration;
use std::thread;

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

use tao::{
    dpi::LogicalSize,
    event::{Event, WindowEvent},
    event_loop::{ControlFlow, EventLoop},
    window::WindowBuilder,
};
use wry::WebViewBuilder;

const CREATE_NO_WINDOW: u32 = 0x08000000;
const SERVER_URL: &str = "http://127.0.0.1:8000";

fn check_server_running() -> bool {
    let client = reqwest::blocking::Client::builder()
        .timeout(Duration::from_millis(600))
        .build();

    if let Ok(client) = client {
        if let Ok(res) = client.get(format!("{}/api/info", SERVER_URL)).send() {
            return res.status().is_success();
        }
    }
    false
}

fn start_backend() -> Option<Child> {
    if check_server_running() {
        println!("Voice AI backend is already running.");
        return None;
    }

    println!("Starting Voice AI backend process...");
    
    let current_dir = std::env::current_dir().unwrap_or_default();
    let working_dir = if current_dir.ends_with("voice_ai_desktop") {
        current_dir.parent().map(|p| p.to_path_buf()).unwrap_or(current_dir)
    } else {
        current_dir
    };

    let mut cmd = Command::new("python");
    cmd.arg("app.py")
        .current_dir(&working_dir);

    #[cfg(target_os = "windows")]
    cmd.creation_flags(CREATE_NO_WINDOW);

    match cmd.spawn() {
        Ok(child) => {
            println!("Backend process spawned (PID: {}). Waiting for startup...", child.id());
            for _ in 0..30 {
                thread::sleep(Duration::from_millis(500));
                if check_server_running() {
                    println!("Backend is healthy and responding!");
                    break;
                }
            }
            Some(child)
        }
        Err(e) => {
            eprintln!("Failed to spawn backend python app.py: {}", e);
            None
        }
    }
}

fn load_app_icon() -> Option<tao::window::Icon> {
    let icon_bytes = include_bytes!("../icon.png");
    if let Ok(img) = image::load_from_memory(icon_bytes) {
        let rgba = img.into_rgba8();
        let (width, height) = rgba.dimensions();
        tao::window::Icon::from_rgba(rgba.into_raw(), width, height).ok()
    } else {
        None
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Launching Voice AI Desktop Application...");

    // Start Python backend
    let backend_child = Arc::new(Mutex::new(start_backend()));

    // Initialize Tao window & event loop
    let event_loop = EventLoop::new();
    let mut window_builder = WindowBuilder::new()
        .with_title("Voice AI - Speech to Text & Kokoro TTS")
        .with_inner_size(LogicalSize::new(1280.0, 860.0))
        .with_min_inner_size(LogicalSize::new(960.0, 600.0))
        .with_resizable(true);

    if let Some(icon) = load_app_icon() {
        window_builder = window_builder.with_window_icon(Some(icon));
    }

    let window = window_builder.build(&event_loop)?;

    // Create Wry WebView inside Tao window
    let builder = WebViewBuilder::new();
    
    #[cfg(target_os = "windows")]
    let builder = builder.with_background_color((2, 6, 23, 255));

    let _webview = builder
        .with_url(SERVER_URL)
        .build(&window)?;

    let event_loop_child = Arc::clone(&backend_child);

    event_loop.run(move |event, _, control_flow| {
        *control_flow = ControlFlow::Wait;

        match event {
            Event::WindowEvent {
                event: WindowEvent::CloseRequested,
                ..
            } => {
                println!("Window close requested. Terminating background services...");
                if let Ok(mut lock) = event_loop_child.lock() {
                    if let Some(mut child) = lock.take() {
                        let _ = child.kill();
                        println!("Backend service stopped.");
                    }
                }
                *control_flow = ControlFlow::Exit;
            }
            _ => (),
        }
    });
}
