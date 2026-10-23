use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    #[cfg(target_os = "windows")]
    {
        // Embed .ico into the compiled Windows .exe binary
        let mut res = winres::WindowsResource::new();
        res.set_icon("icon.ico");
        res.set("ProductName", "Voice AI");
        res.set("FileDescription", "Voice AI - Speech to Text & Kokoro TTS");
        res.set("LegalCopyright", "Copyright (c) 2026");
        let _ = res.compile();

        // Automatically copy WebView2Loader.dll to target directory and project root
        let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());
        if let Some(target_dir) = out_dir.ancestors().nth(3) {
            let release_dll = out_dir.join("x64").join("WebView2Loader.dll");
            if release_dll.exists() {
                let _ = fs::copy(&release_dll, target_dir.join("WebView2Loader.dll"));
                if let Some(project_root) = target_dir.ancestors().nth(2) {
                    let _ = fs::copy(&release_dll, project_root.join("WebView2Loader.dll"));
                }
            }
        }
    }
}
