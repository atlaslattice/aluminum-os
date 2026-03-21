//! Cross-platform terminal rendering — ANSI escape codes
//!
//! Works on:
//!   Linux/macOS  — natively
//!   Windows 10+  — with ENABLE_VIRTUAL_TERMINAL_PROCESSING (auto-enabled below)
//!   Windows <10  — falls back to plain text (no color)
//!
//! No external dependencies.

// ANSI color constants
pub const RESET:  &str = "\x1b[0m";
pub const BOLD:   &str = "\x1b[1m";
pub const DIM:    &str = "\x1b[2m";
pub const GREEN:  &str = "\x1b[32m";
pub const YELLOW: &str = "\x1b[33m";
pub const RED:    &str = "\x1b[31m";
pub const CYAN:   &str = "\x1b[36m";
pub const PURPLE: &str = "\x1b[35m";
#[allow(dead_code)]
pub const BLUE:   &str = "\x1b[34m";
/// Gold = bold yellow — used for Nexus/Forge highlights
pub const GOLD:   &str = "\x1b[33;1m";
/// Forge accent — orange-ish bold (reserved for future use)
#[allow(dead_code)]
pub const FORGE:  &str = "\x1b[38;5;214m";

/// Enable ANSI output on Windows 10+ via winapi.
/// On other platforms this is a no-op.
pub fn enable_ansi_support() {
    #[cfg(target_os = "windows")]
    {
        use std::os::windows::io::AsRawHandle;
        use std::io::Write;
        // SetConsoleMode with ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
        // We use a raw syscall to avoid winapi dependency.
        let handle = std::io::stdout().as_raw_handle();
        unsafe {
            // kernel32: GetConsoleMode + SetConsoleMode
            // If this fails (Win < 10), colors are stripped automatically.
            let mut mode: u32 = 0;
            if GetConsoleMode(handle as _, &mut mode) != 0 {
                SetConsoleMode(handle as _, mode | 0x0004);
            }
        }
    }
}

#[cfg(target_os = "windows")]
extern "system" {
    fn GetConsoleMode(h: *mut std::ffi::c_void, mode: *mut u32) -> i32;
    fn SetConsoleMode(h: *mut std::ffi::c_void, mode: u32) -> i32;
}

/// Print the Forge header banner
pub fn print_header(title: &str, subtitle: &str) {
    println!("{GOLD}╔══════════════════════════════════════════════════════════╗{RESET}");
    println!("{GOLD}║{RESET}  {BOLD}{title:<56}{RESET}{GOLD}║{RESET}");
    println!("{GOLD}║{RESET}  {DIM}{subtitle:<56}{RESET}{GOLD}║{RESET}");
    println!("{GOLD}╚══════════════════════════════════════════════════════════╝{RESET}");
    println!();
}

/// Print a section divider
pub fn print_divider(label: &str) {
    println!("{DIM}── {label} {}{RESET}", "─".repeat(50_usize.saturating_sub(label.len() + 4)));
}

/// Print a key-value pair with aligned formatting
pub fn print_kv(key: &str, value: &str, color: &str) {
    println!("  {DIM}{key:<22}{RESET}  {color}{value}{RESET}");
}

/// Print NPFM score with visual bar
pub fn print_npfm(npfm: f32) {
    let pct = ((npfm + 1.0) / 2.0 * 30.0) as usize; // map -1..1 → 0..30
    let bar: String = (0..30).map(|i| if i < pct { '▓' } else { '░' }).collect();
    let color = if npfm >= 0.3 { GREEN } else if npfm >= 0.0 { YELLOW } else { RED };
    println!("  {DIM}NPFM{RESET}                    {color}{npfm:+.3}  {bar}{RESET}");
}

/// Print a protocol compliance row
pub fn print_protocol(name: &str, compliant: bool, confidence: f32) {
    let (icon, color) = if compliant { ("✓", GREEN) } else { ("✗", RED) };
    let pct = (confidence * 100.0) as u32;
    let bar: String = (0..20).map(|i| if (i as f32) < confidence * 20.0 { '▓' } else { '░' }).collect();
    println!("  {color}{icon}{RESET}  {DIM}{name:<26}{RESET}  {color}{pct:3}%  {bar}{RESET}");
}

/// Print verdict banner
pub fn print_verdict(verdict: &str) {
    let (color, icon) = match verdict {
        "APPROVED"    => (GREEN,  "✓ APPROVED"),
        "CONDITIONAL" => (YELLOW, "◎ CONDITIONAL"),
        _             => (RED,    "✗ REJECTED"),
    };
    println!();
    println!("  {BOLD}{color}Verdict: {icon}{RESET}");
    println!();
}
