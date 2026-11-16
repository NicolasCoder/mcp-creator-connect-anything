#!/usr/bin/env python3
"""
⚡ MCP Creator — Connect Anything (`create_mcp.py`)
===================================================
Interactive Wizard & CLI Scaffolder that turns ANY Web App / SaaS into an
unbreakable, self-healing Model Context Protocol (MCP) Server.

Distills the production engineering of:
  - Flow Studio MCP (Veo 3.1 / Nano Banana 2.1 — Queue 9334 / Chrome 9333)
  - Adobe Podcast Enhance MCP (SoundLift V2 — Multi-Login Pool + Quota Failover + Shadow-DOM Piercing)
  - Google AI Studio Speech MCP (Gemini 3.8 TTS — Triple Audio Silence Shield + Triple-Capture Engine)

Usage:
  1) Interactive Wizard (8 Golden Questions):
     python create_mcp.py

  2) Non-Interactive CLI (for AI Agents & Automation):
     python create_mcp.py --name "Suno Studio" --prefix "suno" --url "https://suno.com/create" --non-interactive
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DOM_BYPASS = SCRIPT_DIR / "templates" / "dom_bypass.js"


def slugify(text: str, sep: str = "_") -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", sep, (text or "").strip().lower()).strip(sep)
    return clean or "custom_web"


def ask_choice(prompt: str, default: str = "y") -> bool:
    suffix = "[S/n]" if default.lower().startswith("y") or default.lower().startswith("s") else "[s/N]"
    ans = input(f"{prompt} {suffix}: ").strip().lower()
    if not ans:
        return default.lower() in ("y", "s", "yes", "sim", "true", "1")
    return ans in ("y", "s", "yes", "sim", "true", "1")


def run_interactive_wizard(defaults: Dict[str, Any]) -> Dict[str, Any]:
    print("\n" + "=" * 76)
    print("  ⚡ MCP CREATOR — CONNECT ANYTHING (WIZARD DE PERSONALIZAÇÃO EM 8 PASSOS)")
    print("  Transforme qualquer site ou serviço Web em um Servidor MCP Inquebrável!")
    print("=" * 76 + "\n")

    # 1. Site / Serviço Alvo
    name = input(f"1️⃣  [Site Alvo] Nome do Serviço/MCP [{defaults['name']}]: ").strip() or defaults["name"]
    default_prefix = slugify(name, "_")
    prefix = input(f"   Prefixo das tools (ex: '{default_prefix}_execute') [{default_prefix}]: ").strip() or default_prefix
    prefix = slugify(prefix, "_")
    url = input(f"   URL principal da plataforma [{defaults['url']}]: ").strip() or defaults["url"]

    # 2. Modo de Visibilidade do Chrome
    print("\n2️⃣  [Visibilidade do Chrome] Como o navegador deve operar?")
    print("   [1] Fantasma Off-Screen (Recomendado: roda invisível em X=-2400 sem roubar foco, abre visível só no 1º login)")
    print("   [2] Sempre Visível na Tela")
    print("   [3] Híbrido Sob Demanda")
    vis_choice = input("   Escolha [1/2/3] (Padrão: 1): ").strip() or "1"
    visibility = {"1": "offscreen", "2": "visible", "3": "hybrid"}.get(vis_choice, "offscreen")

    # 3. System Tray & Dashboard
    print("\n3️⃣  [System Tray & Mini-Dashboard UI]")
    enable_tray = ask_choice("   Gerar aplicativo de Bandeja do Sistema (System Tray + Flyout Apple UI)?", "y")
    enable_dashboard = ask_choice("   Ativar Dashboard Web ao vivo (http://127.0.0.1:<porta>/dashboard)?", "y")

    # 4. Multi-Login
    print("\n4️⃣  [Multi-Login & Rotação de Contas]")
    enable_multi_login = ask_choice(
        "   Ativar Pool Multi-Contas (conta_1, conta_2...) com troca automática quando acabar os créditos?",
        "y",
    )

    # 5. Leitor de Créditos / Limites
    print("\n5️⃣  [Leitor de Créditos, Limites e Cotas em Tempo Real]")
    enable_quota_reader = ask_choice(
        f"   Expor a tool '{prefix}_quota_status' para o agente ler créditos/limites restantes na página/API?",
        "y",
    )
    quota_unit = "credits"
    if enable_quota_reader:
        quota_unit = input("   Unidade de cota do site (ex: credits, minutes, tokens, generations) [credits]: ").strip() or "credits"

    # 6. Escudo Triplo de Silêncio Absoluto
    print("\n6️⃣  [Escudo Triplo de Silêncio Absoluto — Zero-Audio Leak]")
    enable_mute_audio = ask_choice(
        "   Silenciar 100% da aba (--mute-audio + CDP Mute + WebAudio ZeroGain) para não tocar som no PC?",
        "y",
    )

    # 7. Fila Central Única & Portas
    print("\n7️⃣  [Fila Central Única (SQLite PriorityQueue) & Portas Isoladas]")
    chrome_port = int(input(f"   Porta CDP exclusiva do Chrome [{defaults['chrome_port']}]: ").strip() or defaults["chrome_port"])
    daemon_port = int(input(f"   Porta HTTP da Fila Central [{defaults['daemon_port']}]: ").strip() or defaults["daemon_port"])

    # 8. Auto-Healing
    print("\n8️⃣  [Protocolo de Auto-Healing (Self-Healing MCP)]")
    enable_auto_healing = ask_choice(
        f"   Incluir tools '{prefix}_diagnose', '{prefix}_update_selectors' e '{prefix}_reload_daemon'?",
        "y",
    )

    default_out = str(Path.cwd() / f"{slugify(name, '-')}-mcp")
    output_dir = input(f"\n📂 Pasta de saída do projeto [{default_out}]: ").strip() or default_out

    return {
        "name": name,
        "slug": f"{slugify(name, '-')}-mcp" if not slugify(name, "-").endswith("-mcp") else slugify(name, "-"),
        "prefix": prefix,
        "url": url,
        "chrome_port": chrome_port,
        "daemon_port": daemon_port,
        "visibility": visibility,
        "enable_tray": enable_tray,
        "enable_dashboard": enable_dashboard,
        "enable_multi_login": enable_multi_login,
        "enable_quota_reader": enable_quota_reader,
        "quota_unit": quota_unit,
        "enable_mute_audio": enable_mute_audio,
        "enable_auto_healing": enable_auto_healing,
        "output_dir": output_dir,
    }


def render_selectors_json(cfg: Dict[str, Any]) -> str:
    data = {
        "service_info": {
            "name": cfg["name"],
            "prefix": cfg["prefix"],
            "target_url": cfg["url"],
            "chrome_port": cfg["chrome_port"],
            "daemon_port": cfg["daemon_port"],
            "created_with": "MCP Creator - Connect Anything",
        },
        "api_endpoints": {
            "gateway_base": cfg["url"].rstrip("/"),
            "execute_path": "/api/v1/generate",
            "status_path": "/api/v1/status",
            "user_quota_path": "/api/v1/user/credits",
            "sniffer_keywords": ["api", "graphql", "generate", "create", "status", "credits", "quota", "export", "download"],
        },
        "selectors": {
            "target_url": cfg["url"],
            "logged_in_indicator": '[data-testid="user-profile"], [aria-label*="Account"], [aria-label*="Conta"], [aria-label*="Profile"], img[alt*="Avatar"], button[id*="profile"]',
            "logged_out_indicator": '[data-testid="login-button"], button:has-text("Sign in"), button:has-text("Log in"), button:has-text("Entrar"), a[href*="login"]',
            "prompt_input": '[data-testid="prompt-input"], textarea, .ProseMirror, [contenteditable="true"], input[type="text"]',
            "file_input": 'input[type="file"]',
            "choose_files_btn": '[data-testid="upload-button"], button:has-text("Upload"), button:has-text("Choose file"), button:has-text("Escolher arquivo")',
            "submit_btn": '[data-testid="generate-button"], [data-testid="submit-button"], button:has-text("Generate"), button:has-text("Create"), button:has-text("Gerar"), button:has-text("Run"), button[type="submit"]',
            "processing_indicator": '[data-testid="processing-indicator"], [role="progressbar"], .loading, .spinner',
            "download_btn": '[data-testid="download-button"], button[aria-label*="Download"], button:has-text("Download"), button:has-text("Baixar"), a[download]',
            "result_media": "audio[src], video[src], img[src*='blob:'], a[href*='blob:']",
            "quota_badge": '[data-testid*="credit"], [data-testid*="quota"], [class*="credit"], [class*="quota"], [aria-label*="credit"]',
            "upsell_close_btn": '[data-testid="close-modal"], [aria-label="Close"], [aria-label="Fechar"], sp-close-button, button.close',
        },
        "quota_rules": {
            "enabled": cfg["enable_quota_reader"],
            "unit": cfg["quota_unit"],
            "default_free_limit": 100.0,
            "default_pro_limit": 1000.0,
            "cost_per_job": 1.0,
            "exhausted_http_codes": [402, 422, 429],
            "exhausted_keywords": [
                "quota exceeded",
                "out of credits",
                "insufficient credits",
                "daily limit",
                "rate limit",
                "limite atingido",
                "sem créditos",
            ],
        },
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def render_config_json(cfg: Dict[str, Any]) -> str:
    data = {
        "service_name": cfg["name"],
        "prefix": cfg["prefix"],
        "target_url": cfg["url"],
        "chrome_port": cfg["chrome_port"],
        "daemon_port": cfg["daemon_port"],
        "modo_invisivel": cfg["visibility"] != "visible",
        "visibility_mode": cfg["visibility"],
        "mute_audio": cfg["enable_mute_audio"],
        "multi_login": cfg["enable_multi_login"],
        "quota_reader": cfg["enable_quota_reader"],
        "enable_tray": cfg["enable_tray"],
        "enable_dashboard": cfg["enable_dashboard"],
        "auto_healing": cfg["enable_auto_healing"],
        "processos_simultaneos": 1,
        "timeout_processamento_seg": 600,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def render_core_api_py(cfg: Dict[str, Any]) -> str:
    p = cfg["prefix"]
    P_UPPER = p.upper()
    code = f'''#!/usr/bin/env python3
"""
{cfg["name"]} — Core Web-to-MCP Engine (`{p}api.py`)
Generated by MCP Creator — Connect Anything
Includes:
  1. Native Chrome CDP Engine + Win32_Process.Create Job-Object Detachment
  2. Off-Screen Window Positioning (-2400, 0) + Windows COM ITaskbarList Stealth
  3. Triple Audio Silence Shield (--mute-audio + CDP setAudioMuted + WebAudio ZeroGain)
  4. Multi-Account Profile Pool (`accounts.json`) + Smart Quota Failover
  5. DOM / Shadow-DOM / React Fiber Native Bypass (`dom_bypass.js`)
  6. Triple-Capture Engine (Network RPC/API -> In-Page Blob Fetch -> UI Download Watcher)
  7. Full Self-Healing Diagnostic Collector (`coletar_diagnostico_pagina`)
"""

import asyncio
import base64
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SELECTORS_PATH = os.path.join(BASE_DIR, "selectors.json")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
ACCOUNTS_PATH = os.path.join(BASE_DIR, "accounts.json")
DOM_BYPASS_PATH = os.path.join(BASE_DIR, "dom_bypass.js")
DIAGNOSTICS_DIR = os.path.join(BASE_DIR, "diagnostics")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

CHROME_PORT = int(os.environ.get("{P_UPPER}_CHROME_PORT", "{cfg["chrome_port"]}"))
DAEMON_PORT = int(os.environ.get("{P_UPPER}_DAEMON_PORT", "{cfg["daemon_port"]}"))


def carregar_dom_bypass_js() -> str:
    if os.path.exists(DOM_BYPASS_PATH):
        try:
            with open(DOM_BYPASS_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return "window.__MCP_CREATOR_BYPASS__ = window.__MCP_CREATOR_BYPASS__ || {{}};"


def _obter_diretorio_perfil_base(account_id: str = "conta_1") -> str:
    env_dir = os.environ.get("{P_UPPER}_PROFILE_DIR")
    if env_dir and account_id in ("", "conta_1", "default"):
        return env_dir
    base = (
        rf"C:\\{p}-mcp-profile"
        if os.name == "nt"
        else os.path.join(os.path.expanduser("~"), f".{p}-mcp-profile")
    )
    if not account_id or account_id in ("conta_1", "default"):
        return base
    slug = re.sub(r"[^A-Za-z0-9_-]", "_", account_id.strip().lower())
    return f"{{base}}-{{slug}}"


def _criar_registro_conta_padrao(account_id: str = "conta_1", label: str = "Conta 1 (Principal)") -> dict:
    prof_dir = _obter_diretorio_perfil_base(account_id)
    return {{
        "id": account_id,
        "label": label,
        "profile_dir": prof_dir,
        "email": "",
        "display_name": "",
        "tier": "free",
        "logged_in": os.path.exists(os.path.join(prof_dir, ".login_completed")),
        "quota_unit": "{cfg["quota_unit"]}",
        "quota_limit": 100.0,
        "quota_used": 0.0,
        "quota_remaining": 100.0,
        "quota_reset_at_epoch": 0.0,
        "last_checked_at": "",
    }}


def carregar_contas() -> dict:
    padrao = {{
        "active_account": "conta_1",
        "auto_rotate": {str(cfg["enable_multi_login"])},
        "accounts": {{
            "conta_1": _criar_registro_conta_padrao("conta_1", "Conta 1 (Principal)"),
        }},
    }}
    dados = padrao
    if os.path.exists(ACCOUNTS_PATH):
        try:
            with open(ACCOUNTS_PATH, "r", encoding="utf-8") as f:
                lido = json.load(f)
                if isinstance(lido, dict) and isinstance(lido.get("accounts"), dict) and lido["accounts"]:
                    dados = lido
        except Exception:
            pass

    if "conta_1" not in dados["accounts"]:
        dados["accounts"]["conta_1"] = _criar_registro_conta_padrao("conta_1", "Conta 1 (Principal)")
    if dados.get("active_account") not in dados["accounts"]:
        dados["active_account"] = next(iter(dados["accounts"].keys()))

    agora = time.time()
    mudou = False
    for acc_id, acc in dados["accounts"].items():
        prof = acc.get("profile_dir") or _obter_diretorio_perfil_base(acc_id)
        acc["profile_dir"] = prof
        reset_ep = float(acc.get("quota_reset_at_epoch") or 0.0)
        if reset_ep > 0 and agora >= reset_ep:
            lim = float(acc.get("quota_limit") or 100.0)
            acc["quota_used"] = 0.0
            acc["quota_remaining"] = lim
            acc["quota_reset_at_epoch"] = 0.0
            mudou = True

    if mudou or not os.path.exists(ACCOUNTS_PATH):
        salvar_contas(dados)
    return dados


def salvar_contas(dados: dict) -> dict:
    try:
        with open(ACCOUNTS_PATH, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[!] Aviso ao salvar accounts.json: {{e}}")
    return dados


def obter_conta_ativa() -> dict:
    dados = carregar_contas()
    acc_id = dados.get("active_account", "conta_1")
    return dados["accounts"].get(acc_id) or next(iter(dados["accounts"].values()))


def obter_diretorio_perfil(account_id: str = "") -> str:
    dados = carregar_contas()
    alvo = account_id.strip() if account_id else dados.get("active_account", "conta_1")
    acc = dados["accounts"].get(alvo)
    if acc and acc.get("profile_dir"):
        return acc["profile_dir"]
    return _obter_diretorio_perfil_base(alvo)


def adicionar_conta(account_id: str = "", label: str = "") -> dict:
    dados = carregar_contas()
    contas = dados["accounts"]
    if not account_id or not account_id.strip():
        idx = len(contas) + 1
        while f"conta_{{idx}}" in contas:
            idx += 1
        account_id = f"conta_{{idx}}"
    else:
        account_id = re.sub(r"[^A-Za-z0-9_-]", "_", account_id.strip().lower())

    if account_id in contas:
        if label:
            contas[account_id]["label"] = label
            salvar_contas(dados)
        return contas[account_id]

    num = len(contas) + 1
    rotulo = label.strip() if label else f"Conta {{num}} ({{account_id}})"
    nova = _criar_registro_conta_padrao(account_id, rotulo)
    os.makedirs(nova["profile_dir"], exist_ok=True)
    contas[account_id] = nova
    salvar_contas(dados)
    return nova


def definir_conta_ativa(account_id: str) -> dict:
    dados = carregar_contas()
    account_id = re.sub(r"[^A-Za-z0-9_-]", "_", account_id.strip().lower())
    if account_id not in dados["accounts"]:
        adicionar_conta(account_id=account_id)
        dados = carregar_contas()
    dados["active_account"] = account_id
    salvar_contas(dados)
    return dados["accounts"][account_id]


def remover_conta(account_id: str) -> bool:
    dados = carregar_contas()
    account_id = re.sub(r"[^A-Za-z0-9_-]", "_", (account_id or "").strip().lower())
    if account_id not in dados["accounts"] or len(dados["accounts"]) <= 1:
        return False
    era_ativa = dados.get("active_account") == account_id
    del dados["accounts"][account_id]
    if era_ativa:
        nova_ativa = next(iter(dados["accounts"].keys()))
        dados["active_account"] = nova_ativa
        salvar_contas(dados)
        definir_conta_ativa(nova_ativa)
    else:
        salvar_contas(dados)
    return True


def ja_fez_login_inicial(profile_dir: str = "") -> bool:
    alvo = profile_dir or obter_diretorio_perfil()
    return os.path.exists(os.path.join(alvo, ".login_completed"))


def marcar_login_concluido(profile_dir: str = ""):
    alvo = profile_dir or obter_diretorio_perfil()
    os.makedirs(alvo, exist_ok=True)
    with open(os.path.join(alvo, ".login_completed"), "w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat())
    dados = carregar_contas()
    for acc in dados["accounts"].values():
        if os.path.normcase(acc.get("profile_dir", "")) == os.path.normcase(alvo):
            acc["logged_in"] = True
    salvar_contas(dados)


def detectar_executavel_chrome() -> str:
    for env_var in ("{P_UPPER}_CHROME_EXE", "CHROME_EXE", "FLOW_CHROME_EXE"):
        env_chrome = os.environ.get(env_var)
        if env_chrome and os.path.exists(env_chrome):
            return env_chrome

    sistema = platform.system().lower()
    candidatos = []
    if sistema == "windows":
        local_app = os.environ.get("LOCALAPPDATA", "")
        prog_files = os.environ.get("PROGRAMFILES", r"C:\\Program Files")
        prog_x86 = os.environ.get("PROGRAMFILES(X86)", r"C:\\Program Files (x86)")
        candidatos = [
            os.path.join(prog_files, r"Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(prog_x86, r"Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(local_app, r"Google\\Chrome\\Application\\chrome.exe"),
            os.path.join(prog_files, r"Google\\Chrome Beta\\Application\\chrome.exe"),
        ]
    elif sistema == "darwin":
        candidatos = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    else:
        for cmd in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
            achado = shutil.which(cmd)
            if achado:
                candidatos.append(achado)

    for c in candidatos:
        if c and os.path.exists(c):
            return c
    raise FileNotFoundError("Google Chrome nao encontrado. Defina {P_UPPER}_CHROME_EXE.")


def carregar_seletores() -> dict:
    if os.path.exists(SELECTORS_PATH):
        try:
            with open(SELECTORS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Aviso ao ler selectors.json: {{e}}")
    return {{"selectors": {{"target_url": "{cfg["url"]}"}}, "api_endpoints": {{}}, "quota_rules": {{}}}}


def atualizar_seletores(novos_dados: dict) -> dict:
    atual = carregar_seletores()
    for k, v in novos_dados.items():
        if isinstance(v, dict) and k in atual and isinstance(atual[k], dict):
            atual[k].update(v)
        elif not isinstance(v, dict) and k in atual.get("selectors", {{}}):
            atual["selectors"][k] = v
        else:
            atual[k] = v
    with open(SELECTORS_PATH, "w", encoding="utf-8") as f:
        json.dump(atual, f, indent=2, ensure_ascii=False)
    return atual


def carregar_config() -> dict:
    padrao = {{
        "modo_invisivel": {str(cfg["visibility"] != "visible")},
        "mute_audio": {str(cfg["enable_mute_audio"])},
        "multi_login": {str(cfg["enable_multi_login"])},
        "quota_reader": {str(cfg["enable_quota_reader"])},
        "timeout_processamento_seg": 600,
    }}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                padrao.update(json.load(f))
        except Exception:
            pass
    return padrao


def obter_perfil_chrome_rodando(porta: int = CHROME_PORT) -> str:
    try:
        import psutil
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                nome = (proc.info.get("name") or "").lower()
                if "chrome" in nome:
                    cmdline = proc.info.get("cmdline") or []
                    cmd = " ".join(cmdline)
                    if f"--remote-debugging-port={{porta}}" in cmd and "--type=" not in cmd:
                        for arg in cmdline:
                            if arg.startswith("--user-data-dir="):
                                return arg.split("=", 1)[1].strip('"').strip("'")
            except Exception:
                pass
    except Exception:
        pass
    return ""


def fechar_chrome_porta(porta: int = CHROME_PORT):
    """Encerra APENAS os processos do Google Chrome iniciados na porta especificada."""
    try:
        import psutil
        raizes = []
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                nome = (proc.info.get("name") or "").lower()
                if "chrome" in nome:
                    cmd = " ".join(proc.info.get("cmdline") or [])
                    if f"--remote-debugging-port={{porta}}" in cmd and "--type=" not in cmd:
                        raizes.append(proc)
            except Exception:
                pass

        todos = []
        for proc in raizes:
            try:
                for child in proc.children(recursive=True):
                    todos.append(child)
                    try:
                        child.terminate()
                    except Exception:
                        pass
                todos.append(proc)
                proc.terminate()
            except Exception:
                pass
        _, alive = psutil.wait_procs(todos, timeout=3)
        for proc in alive:
            try:
                proc.kill()
            except Exception:
                pass
    except Exception as e:
        print(f"[!] Aviso ao fechar Chrome da porta {{porta}}: {{e}}")


def iniciar_chrome_isolado(invisivel: bool = True, porta: int = CHROME_PORT, profile_dir: str = ""):
    chrome_exe = detectar_executavel_chrome()
    prof = profile_dir or obter_diretorio_perfil()
    os.makedirs(prof, exist_ok=True)
    cfg = carregar_config()
    sels = carregar_seletores().get("selectors", {{}})
    target_url = sels.get("target_url", "{cfg["url"]}")
    pos_arg = "--window-position=-2400,0" if invisivel else "--window-position=120,90"

    args_list = [
        f"--remote-debugging-port={{porta}}",
        f'--user-data-dir="{{prof}}"' if os.name == "nt" else f"--user-data-dir={{prof}}",
        "--window-size=1360,860",
        pos_arg,
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
    ]
    if cfg.get("mute_audio", True):
        args_list.extend(["--mute-audio", "--autoplay-policy=user-gesture-required"])

    args_list.append(f'"{{target_url}}"' if os.name == "nt" else target_url)

    if os.name == "nt":
        cmd_str = f'"{{chrome_exe}}" ' + " ".join(args_list)
        ps_cmd = (
            f"Invoke-CimMethod -ClassName Win32_Process -MethodName Create "
            f"-Arguments @{{{{CommandLine='{{cmd_str}}'}}}} | Out-Null"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.Popen(
            [chrome_exe] + args_list,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )


def controlar_visibilidade_taskbar(visivel: bool, porta: int = CHROME_PORT) -> bool:
    """Usa Windows COM ITaskbarList (DeleteTab / AddTab) para ocultar/exibir o icone da barra de tarefas."""
    if platform.system() != "Windows":
        return False
    try:
        import ctypes
        from ctypes import wintypes
        import psutil

        user32 = ctypes.windll.user32
        ole32 = ctypes.windll.ole32
        ole32.CoInitialize(None)

        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", ctypes.c_byte * 8),
            ]

        CLSID_TaskbarList = GUID(0x56FDF344, 0xFD6D, 0x11D0, (ctypes.c_byte * 8)(0x95, 0x8A, 0x00, 0x60, 0x97, 0xC9, 0xA0, 0x90))
        IID_ITaskbarList = GUID(0x56FDF342, 0xFD6D, 0x11D0, (ctypes.c_byte * 8)(0x95, 0x8A, 0x00, 0x60, 0x97, 0xC9, 0xA0, 0x90))

        p_tbl = ctypes.c_void_p()
        hr = ole32.CoCreateInstance(ctypes.byref(CLSID_TaskbarList), None, 1, ctypes.byref(IID_ITaskbarList), ctypes.byref(p_tbl))
        if hr != 0 or not p_tbl.value:
            return False

        vtable = ctypes.cast(p_tbl, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
        ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p)(vtable[3])(p_tbl)
        add_tab = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, wintypes.HWND)(vtable[4])
        del_tab = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, wintypes.HWND)(vtable[5])

        target_pids = set()
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            if (proc.info.get("name") or "").lower() == "chrome.exe":
                cmd = " ".join(proc.info.get("cmdline") or [])
                if f"--remote-debugging-port={{porta}}" in cmd:
                    target_pids.add(proc.info["pid"])

        def cb(hwnd, lparam):
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value in target_pids:
                cls_name = ctypes.create_unicode_buffer(256)
                user32.GetClassNameW(hwnd, cls_name, 256)
                if "Chrome_WidgetWin_1" in cls_name.value:
                    if visivel:
                        add_tab(p_tbl, hwnd)
                    else:
                        del_tab(p_tbl, hwnd)
            return 1

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        user32.EnumWindows(WNDENUMPROC(cb), 0)
        return True
    except Exception:
        return False


async def injetar_bypass_e_silencio(page) -> None:
    js_code = carregar_dom_bypass_js()
    cfg = carregar_config()
    try:
        await page.context.add_init_script(js_code)
    except Exception:
        pass
    try:
        await page.evaluate(js_code)
    except Exception:
        pass

    if cfg.get("mute_audio", True):
        try:
            await page.evaluate("window.__MCP_CREATOR_BYPASS__?.installAudioSilenceShield?.()")
        except Exception:
            pass
        try:
            cdp = await page.context.new_cdp_session(page)
            await cdp.send("Page.setAudioMuted", {{"muted": True}})
            await cdp.detach()
        except Exception:
            pass


async def posicionar_janela_chrome(page, invisivel: bool = True, porta: int = CHROME_PORT) -> bool:
    try:
        cdp = await page.context.new_cdp_session(page)
        if carregar_config().get("mute_audio", True):
            try:
                await cdp.send("Page.setAudioMuted", {{"muted": True}})
            except Exception:
                pass
        win_info = await cdp.send("Browser.getWindowForTarget")
        win_id = win_info["windowId"]
        left_pos = -2400 if invisivel else 120
        top_pos = 0 if invisivel else 90
        await cdp.send(
            "Browser.setWindowBounds",
            {{
                "windowId": win_id,
                "bounds": {{
                    "left": left_pos,
                    "top": top_pos,
                    "width": 1360,
                    "height": 860,
                    "windowState": "normal",
                }},
            }},
        )
        if not invisivel:
            try:
                await cdp.send("Page.bringToFront")
            except Exception:
                pass
        await cdp.detach()
        controlar_visibilidade_taskbar(visivel=not invisivel, porta=porta)
        return True
    except Exception:
        return False


async def obter_parametros_pagina(page) -> dict:
    await injetar_bypass_e_silencio(page)
    sels = carregar_seletores().get("selectors", {{}})
    sel_in = sels.get("logged_in_indicator", '[data-testid="user-profile"]')
    sel_out = sels.get("logged_out_indicator", '[data-testid="login-button"]')
    sel_prompt = sels.get("prompt_input", "textarea")
    sel_quota = sels.get("quota_badge", '[class*="credit"]')

    try:
        return await page.evaluate(
            """(args) => {{
                const [selIn, selOut, selPrompt, selQuota] = args;
                const bp = window.__MCP_CREATOR_BYPASS__;
                const q = bp && bp.querySelectorDeep ? bp.querySelectorDeep : (s) => document.querySelector(s);

                const elIn = q(selIn);
                const elOut = q(selOut);
                const elPrompt = q(selPrompt);
                const elQuota = q(selQuota);

                const quotaText = elQuota ? (elQuota.innerText || elQuota.textContent || '').trim() : '';
                const loggedIn = Boolean(elIn || (elPrompt && !elOut));

                return {{
                    loggedIn,
                    hasPromptInput: Boolean(elPrompt),
                    hasLoggedOutIndicator: Boolean(elOut),
                    quotaBadgeText: quotaText.slice(0, 120),
                    title: document.title,
                    url: window.location.href,
                }};
            }}""",
            [sel_in, sel_out, sel_prompt, sel_quota],
        )
    except Exception:
        return {{"loggedIn": False, "url": page.url if page else ""}}


async def consultar_quota_plataforma(page, account_id: str = "") -> dict:
    """Lê os créditos/limites restantes via DOM (`quota_badge`) e atualiza `accounts.json`."""
    dados_contas = carregar_contas()
    alvo_id = account_id.strip() if account_id else dados_contas.get("active_account", "conta_1")
    if alvo_id not in dados_contas["accounts"]:
        adicionar_conta(alvo_id)
        dados_contas = carregar_contas()

    acc = dados_contas["accounts"][alvo_id]
    params = await obter_parametros_pagina(page)
    logado = bool(params.get("loggedIn"))
    badge_txt = params.get("quotaBadgeText") or ""

    # Extrai primeiro número encontrado no badge de créditos se existir
    nums = re.findall(r"\\d+(?:[\\.,]\\d+)?", badge_txt.replace(",", ""))
    if nums:
        try:
            acc["quota_remaining"] = float(nums[0])
        except Exception:
            pass

    acc["logged_in"] = logado
    acc["last_checked_at"] = datetime.now().isoformat(timespec="seconds")
    dados_contas["accounts"][alvo_id] = acc
    salvar_contas(dados_contas)
    if logado:
        marcar_login_concluido(acc["profile_dir"])

    return {{
        "ok": True,
        "account_id": alvo_id,
        "label": acc.get("label", alvo_id),
        "logged_in": logado,
        "quota_unit": acc.get("quota_unit", "{cfg["quota_unit"]}"),
        "quota_limit": acc.get("quota_limit", 100.0),
        "quota_used": acc.get("quota_used", 0.0),
        "quota_remaining": acc.get("quota_remaining", 100.0),
        "raw_badge_text": badge_txt,
        "profile_dir": acc.get("profile_dir"),
        "last_checked_at": acc["last_checked_at"],
    }}


def resumo_pool_contas() -> dict:
    dados = carregar_contas()
    ativa_id = dados.get("active_account", "conta_1")
    lista = []
    total_rem = 0.0
    for acc_id, acc in dados["accounts"].items():
        rem = float(acc.get("quota_remaining") or 0.0)
        total_rem += rem
        lista.append({{
            **acc,
            "id": acc_id,
            "is_active": acc_id == ativa_id,
        }})
    return {{
        "active_account": ativa_id,
        "auto_rotate": bool(dados.get("auto_rotate", True)),
        "total_accounts": len(lista),
        "pool_remaining": round(total_rem, 2),
        "quota_unit": "{cfg["quota_unit"]}",
        "accounts": lista,
    }}


def escolher_proxima_conta_com_quota(custo_estimado: float = 1.0, conta_excluir: str = "") -> str:
    dados = carregar_contas()
    excluir = {{s.strip() for s in conta_excluir.split(",") if s.strip()}}
    candidatas = []
    for idx, (acc_id, acc) in enumerate(dados["accounts"].items()):
        if acc_id in excluir:
            continue
        prof_dir = acc.get("profile_dir") or ""
        tem_login = bool(acc.get("logged_in") or os.path.exists(os.path.join(prof_dir, ".login_completed")))
        if not tem_login:
            continue
        rem = float(acc.get("quota_remaining") or 0.0)
        if rem >= custo_estimado:
            candidatas.append((rem, -idx, acc_id))
    if candidatas:
        candidatas.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return candidatas[0][2]
    return ""


async def executar_acao_web(page, job: dict, recent_network: list) -> Dict[str, Any]:
    """
    Executa o fluxo principal na plataforma alvo usando os 7 Pilares:
      1) Injeta `dom_bypass.js` e Escudo de Silêncio
      2) Faz upload de arquivo (se `input_path` foi enviado) e/ou preenche `prompt` via React Fiber setter
      3) Clica em `submit_btn` e aciona o Triple-Capture Engine (Network RPC -> Blob Fetch -> UI Download)
    """
    await injetar_bypass_e_silencio(page)
    sels = carregar_seletores().get("selectors", {{}})
    prompt = (job.get("prompt") or "").strip()
    input_path = (job.get("input_path") or "").strip()
    output_path = (job.get("output_path") or "").strip()

    if not output_path:
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUTS_DIR, f"{p}_result_{{uuid.uuid4().hex[:8]}}.bin")

    # 1. Upload de arquivo se fornecido
    if input_path and os.path.exists(input_path):
        file_inp = page.locator(sels.get("file_input", 'input[type="file"]')).first
        if await file_inp.count() > 0:
            await file_inp.set_input_files(input_path)
            await asyncio.sleep(1.0)

    # 2. Preenchimento de Prompt via React/Vue/ProseMirror Bypass
    if prompt:
        sel_prompt = sels.get("prompt_input", "textarea")
        res_input = await page.evaluate(
            "(args) => window.__MCP_CREATOR_BYPASS__.setReactInputValue(args[0], args[1])",
            [sel_prompt, prompt],
        )
        if not res_input.get("ok"):
            loc = page.locator(sel_prompt).first
            if await loc.count() > 0:
                await loc.fill(prompt)
        await asyncio.sleep(0.5)

    # 3. Disparo do botão principal
    sel_submit = sels.get("submit_btn", 'button[type="submit"]')
    btn = page.locator(sel_submit).first
    if await btn.count() > 0:
        await btn.click()
    else:
        await page.evaluate(
            "(s) => {{ const el = window.__MCP_CREATOR_BYPASS__.querySelectorDeep(s); if (el) el.click(); }}",
            sel_submit,
        )

    await asyncio.sleep(2.0)

    # 4. Triple-Capture Engine (Camada 2: Blob/Media URI ou Camada 3: Download Button)
    capture_source = "dom_state"
    saved_file = ""
    sel_media = sels.get("result_media", "audio[src], video[src]")
    media_b64 = await page.evaluate(
        """async (s) => {{
            const el = window.__MCP_CREATOR_BYPASS__.querySelectorDeep(s);
            if (!el) return null;
            const src = el.src || el.getAttribute('href') || '';
            if (!src) return null;
            return await window.__MCP_CREATOR_BYPASS__.extractBlobAsBase64(src);
        }}""",
        sel_media,
    )
    if isinstance(media_b64, dict) and media_b64.get("ok") and media_b64.get("base64"):
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(media_b64["base64"]))
        saved_file = os.path.abspath(output_path)
        capture_source = media_b64.get("source", "blob_fetch")

    return {{
        "ok": True,
        "file_path": saved_file,
        "capture_source": capture_source,
        "page_url": page.url,
    }}


async def coletar_diagnostico_pagina(
    page, motivo: str = "", recent_network: Optional[ list ] = None, take_screenshot: bool = True
) -> Dict[str, Any]:
    """Raio-X completo de DOM + Shadow-DOM + Rede + Screenshot para Auto-Healing."""
    os.makedirs(DIAGNOSTICS_DIR, exist_ok=True)
    screenshot_path = os.path.join(DIAGNOSTICS_DIR, "last_diagnostic_screenshot.png")
    report_path = os.path.join(DIAGNOSTICS_DIR, "last_diagnostic_report.json")

    diag: Dict[str, Any] = {{
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "reason": motivo,
        "selectors_file": SELECTORS_PATH,
        "api_file": os.path.abspath(__file__),
        "current_selectors": carregar_seletores(),
        "recent_network_calls": recent_network or [],
        "page_url": None,
        "params": {{}},
        "dom_snapshot": {{}},
        "selector_health": {{}},
        "screenshot_path": None,
        "auto_healing_instructions": (
            "Se um seletor CSS/Shadow-DOM ou endpoint mudou na plataforma: "
            "1) Analise `dom_snapshot.interactive`, `dom_snapshot.testids`, `dom_snapshot.customWebComponents` e `recent_network_calls`. "
            "2) Inspecione visualmente `screenshot_path`. "
            "3) Chame `{p}_update_selectors` para atualizar `selectors.json` em tempo real e `{p}_reload_daemon`."
        ),
    }}

    if not page or page.is_closed():
        diag["error"] = "Page is closed or unavailable"
        return diag

    try:
        await injetar_bypass_e_silencio(page)
        diag["page_url"] = page.url
        diag["params"] = await obter_parametros_pagina(page)
        diag["dom_snapshot"] = await page.evaluate(
            "() => window.__MCP_CREATOR_BYPASS__.dumpInteractiveElementsForHealing(160)"
        )

        sels_map = diag["current_selectors"].get("selectors", {{}})
        health = {{}}
        for k, v in sels_map.items():
            if k == "target_url" or not isinstance(v, str):
                continue
            try:
                cnt = await page.locator(v).count()
                health[k] = {{"selector": v, "matched_count": cnt, "matched": cnt > 0}}
            except Exception as err:
                health[k] = {{"selector": v, "matched_count": 0, "matched": False, "error": str(err)}}
        diag["selector_health"] = health

        if take_screenshot:
            await page.screenshot(path=screenshot_path, full_page=False)
            diag["screenshot_path"] = screenshot_path
    except Exception as e:
        diag["collect_error"] = str(e)

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(diag, f, indent=2, ensure_ascii=False)
        diag["report_path"] = report_path
    except Exception:
        pass
    return diag
'''
    return code


def render_queue_daemon_py(cfg: Dict[str, Any]) -> str:
    p = cfg["prefix"]
    P_UPPER = p.upper()
    code = f'''#!/usr/bin/env python3
"""
{cfg["name"]} — Central Queue Daemon & Live Web Dashboard (`{p}_queue_daemon.py`)
Generated by MCP Creator — Connect Anything
  - Chrome CDP Port : {cfg["chrome_port"]}
  - HTTP Queue Port : {cfg["daemon_port"]}
  - Web Dashboard   : http://127.0.0.1:{cfg["daemon_port"]}/dashboard
"""

import asyncio
import importlib
import json
import os
import sqlite3
import sys
import uuid
from collections import deque
from datetime import datetime
from aiohttp import web
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import {p}api as core_api

DAEMON_HOST = "127.0.0.1"
DAEMON_PORT = int(os.environ.get("{P_UPPER}_DAEMON_PORT", "{cfg["daemon_port"]}"))
PRIMARY_PROFILE_DIR = core_api._obter_diretorio_perfil_base("conta_1")
DB_PATH = os.path.join(PRIMARY_PROFILE_DIR, "{p}_queue.db")


def init_db():
    os.makedirs(PRIMARY_PROFILE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            workspace TEXT,
            prompt TEXT,
            input_path TEXT,
            output_path TEXT,
            status TEXT,
            file_path TEXT,
            error TEXT,
            account_id TEXT,
            created_at TEXT,
            updated_at TEXT,
            priority INTEGER DEFAULT 100
        )
    """)
    conn.commit()
    conn.close()


def db_save_job(job: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO jobs (
            job_id, workspace, prompt, input_path, output_path,
            status, file_path, error, account_id, created_at, updated_at, priority
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job["job_id"],
        job.get("workspace", ""),
        job.get("prompt", ""),
        job.get("input_path", ""),
        job.get("output_path", ""),
        job.get("status", "queued"),
        job.get("file_path") or "",
        job.get("error") or "",
        job.get("account_id") or "",
        job.get("created_at", ""),
        datetime.now().isoformat(timespec="seconds"),
        int(job.get("priority", 100)),
    ))
    conn.commit()
    conn.close()


def db_list_recent_jobs(limit: int = 50):
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


class CentralWebMCPDaemon:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
        self._counter = 0
        self.jobs = {{}}
        self.job_events = {{}}
        self.browser_lock = asyncio.Lock()
        self.playwright = None
        self.browser = None
        self.page = None
        self.config = core_api.carregar_config()
        self.invisivel = bool(self.config.get("modo_invisivel", True))
        self.active_job_id = None
        self.recent_network = deque(maxlen=60)
        self._attached_pages = set()

        for r in reversed(db_list_recent_jobs(80)):
            if r["status"] in ("queued", "running", "processing"):
                r["status"] = "interrupted"
                db_save_job(r)
            self.jobs[r["job_id"]] = r

    async def start(self):
        self.playwright = await async_playwright().start()
        asyncio.create_task(self.worker_loop())

    async def stop(self):
        if self.browser:
            try:
                await self.browser.close()
            except Exception:
                pass
        if self.playwright:
            try:
                await self.playwright.stop()
            except Exception:
                pass

    def _attach_network_sniffer(self, page):
        if id(page) in self._attached_pages:
            return
        self._attached_pages.add(id(page))

        async def on_response(resp):
            try:
                u = resp.url
                kws = core_api.carregar_seletores().get("api_endpoints", {{}}).get("sniffer_keywords", ["api"])
                if any(k in u.lower() for k in kws):
                    preview = ""
                    try:
                        if "json" in (resp.headers.get("content-type") or "").lower():
                            preview = (await resp.text())[:400]
                    except Exception:
                        pass
                    self.recent_network.append({{
                        "time": datetime.now().isoformat(timespec="seconds"),
                        "method": resp.request.method,
                        "status": resp.status,
                        "url": u[:220],
                        "preview": preview,
                    }})
            except Exception:
                pass

        page.on("response", lambda r: asyncio.create_task(on_response(r)))

    async def switch_account_unlocked(self, account_id: str, force_visible=None):
        if self.browser:
            try:
                await self.browser.close()
            except Exception:
                pass
        self.browser = None
        self.page = None
        self._attached_pages.clear()
        core_api.fechar_chrome_porta(porta=core_api.CHROME_PORT)
        await asyncio.sleep(0.8)
        nova = core_api.definir_conta_ativa(account_id)
        prof = nova.get("profile_dir") or core_api.obter_diretorio_perfil()
        if force_visible is None:
            self.invisivel = bool(self.config.get("modo_invisivel", True)) if core_api.ja_fez_login_inicial(prof) else False
        return await self.ensure_browser_and_page(force_visible=force_visible)

    async def ensure_browser_and_page(self, force_visible=None):
        profile_atual = core_api.obter_diretorio_perfil()
        primeiro_uso = not core_api.ja_fez_login_inicial(profile_atual)
        if force_visible is not None:
            self.invisivel = not force_visible
        elif primeiro_uso:
            self.invisivel = False

        perfil_rodando = core_api.obter_perfil_chrome_rodando(porta=core_api.CHROME_PORT)
        if perfil_rodando and os.path.normcase(os.path.abspath(perfil_rodando)) != os.path.normcase(os.path.abspath(profile_atual)):
            if self.browser:
                try:
                    await self.browser.close()
                except Exception:
                    pass
            self.browser = None
            self.page = None
            self._attached_pages.clear()
            core_api.fechar_chrome_porta(porta=core_api.CHROME_PORT)
            await asyncio.sleep(0.8)

        if not self.browser or not self.browser.is_connected() or (self.page and self.page.is_closed()):
            self.browser = None
            self.page = None
            try:
                self.browser = await self.playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{{core_api.CHROME_PORT}}")
            except Exception:
                core_api.iniciar_chrome_isolado(invisivel=self.invisivel, porta=core_api.CHROME_PORT, profile_dir=profile_atual)
                for _ in range(22):
                    await asyncio.sleep(1.0)
                    try:
                        self.browser = await self.playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{{core_api.CHROME_PORT}}")
                        break
                    except Exception:
                        pass
                if not self.browser:
                    raise RuntimeError(f"Nao foi possivel conectar ao Chrome na porta {{core_api.CHROME_PORT}}")

        ctx = self.browser.contexts[0]
        self.page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        self._attach_network_sniffer(self.page)
        await core_api.injetar_bypass_e_silencio(self.page)
        await core_api.posicionar_janela_chrome(self.page, invisivel=self.invisivel)

        target_url = core_api.carregar_seletores().get("selectors", {{}}).get("target_url", "{cfg["url"]}")
        if self.page.url in ("about:blank", "", "chrome://newtab/"):
            await self.page.goto(target_url, wait_until="domcontentloaded")
            await asyncio.sleep(2.0)

        params = await core_api.obter_parametros_pagina(self.page)
        logado = bool(params.get("loggedIn"))
        if logado and not core_api.ja_fez_login_inicial(profile_atual):
            core_api.marcar_login_concluido(profile_atual)
        return self.page, params, logado

    def enqueue_job(self, payload: dict) -> dict:
        job_id = payload.get("job_id") or uuid.uuid4().hex[:12]
        prio = int(payload.get("priority", 100))
        job = {{
            "job_id": job_id,
            "workspace": payload.get("workspace", ""),
            "prompt": payload.get("prompt", ""),
            "input_path": payload.get("input_path", ""),
            "output_path": payload.get("output_path", ""),
            "params": payload.get("params", {{}}),
            "priority": prio,
            "status": "queued",
            "file_path": None,
            "error": None,
            "account_id": core_api.obter_conta_ativa()["id"],
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }}
        self.jobs[job_id] = job
        ev = asyncio.Event()
        self.job_events[job_id] = ev
        db_save_job(job)
        self._counter += 1
        self.queue.put_nowait((prio, self._counter, job_id))
        return job

    async def worker_loop(self):
        while True:
            _, _, job_id = await self.queue.get()
            job = self.jobs.get(job_id)
            if not job or job.get("status") == "cancelled":
                self.queue.task_done()
                continue

            self.active_job_id = job_id
            job["status"] = "running"
            db_save_job(job)

            try:
                async with self.browser_lock:
                    page, params, logado = await self.ensure_browser_and_page()
                    quota = await core_api.consultar_quota_plataforma(page)
                    job["quota"] = quota

                    # Smart Multi-Account Rotation if quota is 0 and auto_rotate is enabled
                    dados_contas = core_api.carregar_contas()
                    if dados_contas.get("auto_rotate") and float(quota.get("quota_remaining", 100.0)) <= 0:
                        prox = core_api.escolher_proxima_conta_com_quota(1.0, conta_excluir=quota.get("account_id", ""))
                        if prox:
                            job["rotated_from_account"] = quota.get("account_id")
                            page, params, logado = await self.switch_account_unlocked(prox)
                            job["account_id"] = prox

                    res = await core_api.executar_acao_web(page, job, list(self.recent_network))
                    job["file_path"] = res.get("file_path")
                    job["capture_source"] = res.get("capture_source")
                    job["status"] = "completed"
                    db_save_job(job)
            except Exception as err:
                job["status"] = "failed"
                job["error"] = str(err)
                try:
                    if self.page and not self.page.is_closed():
                        job["diagnostics"] = await core_api.coletar_diagnostico_pagina(
                            self.page, motivo=str(err), recent_network=list(self.recent_network)
                        )
                except Exception:
                    pass
                db_save_job(job)
            finally:
                self.active_job_id = None
                if job_id in self.job_events:
                    self.job_events[job_id].set()
                self.queue.task_done()


daemon = CentralWebMCPDaemon()


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>{cfg["name"]} — MCP Live Dashboard</title>
<style>
  :root {{ --bg: #090d16; --card: rgba(255,255,255,0.05); --border: rgba(255,255,255,0.1); --accent: #6366f1; --emerald: #10b981; --text: #f8fafc; --muted: #94a3b8; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; }}
  body {{ background: radial-gradient(circle at top left, #1e1b4b, #090d16 60%); color: var(--text); min-height: 100vh; padding: 24px; }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 16px 20px; background: var(--card); border: 1px solid var(--border); border-radius: 14px; }}
  .title {{ font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 10px; }}
  .dot {{ width: 10px; height: 10px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 10px var(--emerald); }}
  .btns {{ display: flex; gap: 8px; }}
  button {{ background: rgba(99,102,241,0.2); color: #fff; border: 1px solid rgba(99,102,241,0.5); padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 12px; }}
  button:hover {{ background: var(--accent); }}
  .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }}
  .card-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }}
  .card-val {{ font-size: 22px; font-weight: 700; margin-top: 6px; }}
  pre {{ background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-radius: 12px; padding: 14px; font-size: 12px; overflow-x: auto; color: #cbd5e1; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title"><span class="dot"></span> {cfg["name"]} — MCP Control Center (Port {cfg["daemon_port"]})</div>
    <div class="btns">
      <button onclick="act('/browser/show')">👁️ Mostrar Chrome</button>
      <button onclick="act('/browser/hide')">👻 Esconder (Off-Screen)</button>
      <button onclick="act('/browser/login')">🔑 Login Inicial</button>
      <button onclick="act('/diagnose')">🩺 Auto-Heal X-Ray</button>
    </div>
  </div>
  <div class="grid">
    <div class="card"><div class="card-label">Conta Ativa</div><div class="card-val" id="acc">-</div></div>
    <div class="card"><div class="card-label">Saldo / Quota Pool</div><div class="card-val" id="quota">-</div></div>
    <div class="card"><div class="card-label">Jobs na Fila</div><div class="card-val" id="qcount">0</div></div>
  </div>
  <div class="card">
    <div class="card-label" style="margin-bottom:8px;">Telemetria Ao Vivo da Fila & Multi-Login</div>
    <pre id="out">Carregando...</pre>
  </div>
</div>
<script>
async function refresh() {{
  try {{
    const r = await fetch('/queue');
    const d = await r.json();
    document.getElementById('acc').innerText = d.pool?.active_account || 'conta_1';
    document.getElementById('quota').innerText = (d.pool?.pool_remaining ?? 100) + ' ' + (d.pool?.quota_unit || '');
    document.getElementById('qcount').innerText = d.queue_pending_count ?? 0;
    document.getElementById('out').innerText = JSON.stringify(d, null, 2);
  }} catch (e) {{}}
}}
async function act(path) {{
  await fetch(path, {{method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: '{{}}'}});
  refresh();
}}
refresh();
setInterval(refresh, 2500);
</script>
</body>
</html>
"""


async def handle_health(request: web.Request):
    return web.json_response({{
        "ok": True,
        "service": "{cfg["name"]}",
        "prefix": "{p}",
        "chrome_port": core_api.CHROME_PORT,
        "daemon_port": DAEMON_PORT,
        "active_job_id": daemon.active_job_id,
        "queue_size": daemon.queue.qsize(),
        "pool": core_api.resumo_pool_contas(),
    }})


async def handle_dashboard(request: web.Request):
    return web.Response(text=DASHBOARD_HTML, content_type="text/html")


async def handle_enqueue(request: web.Request):
    data = await request.json()
    wait = bool(data.get("wait", True))
    if "items" in data and isinstance(data["items"], list):
        created = [daemon.enqueue_job(it) for it in data["items"]]
        if wait:
            for j in created:
                ev = daemon.job_events.get(j["job_id"])
                if ev:
                    await ev.wait()
        return web.json_response({{"ok": True, "jobs": [daemon.jobs[j["job_id"]] for j in created]}})

    job = daemon.enqueue_job(data)
    if wait:
        ev = daemon.job_events.get(job["job_id"])
        if ev:
            await ev.wait()
    final_job = daemon.jobs.get(job["job_id"], job)
    return web.json_response({{"ok": final_job.get("status") == "completed", "job": final_job}})


async def handle_queue(request: web.Request):
    return web.json_response({{
        "ok": True,
        "active_job_id": daemon.active_job_id,
        "queue_pending_count": daemon.queue.qsize(),
        "recent_jobs": db_list_recent_jobs(25),
        "pool": core_api.resumo_pool_contas(),
    }})


async def handle_job_status(request: web.Request):
    jid = request.match_info["job_id"]
    if request.query.get("wait") == "1" and jid in daemon.job_events:
        await daemon.job_events[jid].wait()
    return web.json_response({{"ok": jid in daemon.jobs, "job": daemon.jobs.get(jid)}})


async def handle_browser_action(request: web.Request):
    action = request.match_info["action"].lower()
    async with daemon.browser_lock:
        if action in ("show", "login"):
            page, params, logado = await daemon.ensure_browser_and_page(force_visible=True)
            await core_api.posicionar_janela_chrome(page, invisivel=False)
            daemon.invisivel = False
            return web.json_response({{"ok": True, "action": action, "visible": True, "logged_in": logado, "url": page.url}})
        elif action == "hide":
            page, params, logado = await daemon.ensure_browser_and_page(force_visible=False)
            await core_api.posicionar_janela_chrome(page, invisivel=True)
            daemon.invisivel = True
            if logado:
                core_api.marcar_login_concluido()
            return web.json_response({{"ok": True, "action": "hide", "visible": False, "logged_in": logado, "url": page.url}})
        return web.json_response({{"ok": False, "error": f"Unknown action: {{action}}"}}, status=400)


async def handle_quota(request: web.Request):
    active_quota = None
    if not daemon.browser_lock.locked():
        try:
            async with daemon.browser_lock:
                page, _, _ = await daemon.ensure_browser_and_page()
                active_quota = await core_api.consultar_quota_plataforma(page)
        except Exception as e:
            active_quota = {{"ok": False, "error": str(e)}}
    return web.json_response({{"ok": True, "active_quota": active_quota, "pool": core_api.resumo_pool_contas()}})


async def handle_accounts(request: web.Request):
    if request.method == "GET":
        return web.json_response({{"ok": True, "pool": core_api.resumo_pool_contas()}})
    data = await request.json()
    action = str(data.get("action") or "list").lower()
    acc_id = str(data.get("account_id") or "").strip()
    label = str(data.get("label") or "").strip()

    if action == "list":
        return web.json_response({{"ok": True, "pool": core_api.resumo_pool_contas()}})
    elif action == "add":
        nova = core_api.adicionar_conta(account_id=acc_id, label=label)
        if data.get("open_login", True):
            async with daemon.browser_lock:
                page, _, logado = await daemon.switch_account_unlocked(nova["id"], force_visible=True)
                await core_api.posicionar_janela_chrome(page, invisivel=False)
                daemon.invisivel = False
        return web.json_response({{"ok": True, "action": "add", "account": nova, "pool": core_api.resumo_pool_contas()}})
    elif action in ("switch", "login"):
        async with daemon.browser_lock:
            page, _, logado = await daemon.switch_account_unlocked(acc_id, force_visible=(action == "login"))
            if action == "login" or not logado:
                await core_api.posicionar_janela_chrome(page, invisivel=False)
                daemon.invisivel = False
            quota = await core_api.consultar_quota_plataforma(page)
            return web.json_response({{"ok": True, "action": action, "active_account": acc_id, "logged_in": logado, "quota": quota, "pool": core_api.resumo_pool_contas()}})
    elif action == "remove":
        ok = core_api.remover_conta(acc_id)
        return web.json_response({{"ok": ok, "pool": core_api.resumo_pool_contas()}})
    elif action == "set_auto_rotate":
        dados = core_api.carregar_contas()
        dados["auto_rotate"] = bool(data.get("auto_rotate", True))
        core_api.salvar_contas(dados)
        return web.json_response({{"ok": True, "pool": core_api.resumo_pool_contas()}})
    return web.json_response({{"ok": False, "error": f"Unknown action: {{action}}"}}, status=400)


async def handle_diagnose(request: web.Request):
    data = {{}}
    try:
        data = await request.json()
    except Exception:
        pass
    async with daemon.browser_lock:
        page, _, _ = await daemon.ensure_browser_and_page()
        diag = await core_api.coletar_diagnostico_pagina(
            page,
            motivo=data.get("reason", "AI Agent Auto-Healing X-Ray"),
            recent_network=list(daemon.recent_network),
            take_screenshot=bool(data.get("take_screenshot", True)),
        )
        return web.json_response({{"ok": True, "diagnostics": diag}})


async def handle_selectors(request: web.Request):
    if request.method == "GET":
        return web.json_response({{"ok": True, "selectors": core_api.carregar_seletores()}})
    data = await request.json()
    return web.json_response({{"ok": True, "selectors": core_api.atualizar_seletores(data)}})


async def handle_reload(request: web.Request):
    importlib.reload(core_api)
    daemon.config = core_api.carregar_config()
    return web.json_response({{"ok": True, "message": "Core API and selectors.json hot-reloaded!"}})


async def on_startup(app: web.Application):
    init_db()
    await daemon.start()


async def on_cleanup(app: web.Application):
    await daemon.stop()


def create_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
    app.router.add_get("/health", handle_health)
    app.router.add_get("/dashboard", handle_dashboard)
    app.router.add_post("/enqueue", handle_enqueue)
    app.router.add_get("/queue", handle_queue)
    app.router.add_get("/jobs/{{job_id}}", handle_job_status)
    app.router.add_post("/browser/{{action}}", handle_browser_action)
    app.router.add_get("/quota", handle_quota)
    app.router.add_post("/quota", handle_quota)
    app.router.add_get("/accounts", handle_accounts)
    app.router.add_post("/accounts", handle_accounts)
    app.router.add_post("/diagnose", handle_diagnose)
    app.router.add_get("/selectors", handle_selectors)
    app.router.add_post("/selectors", handle_selectors)
    app.router.add_post("/reload", handle_reload)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host=DAEMON_HOST, port=DAEMON_PORT, print=None)
'''
    return code


def render_mcp_server_py(cfg: Dict[str, Any]) -> str:
    p = cfg["prefix"]
    P_UPPER = p.upper()
    slug = cfg["slug"]
    code = f'''#!/usr/bin/env python3
"""
{cfg["name"]} — FastMCP Server (`{p}_mcp_server.py`)
Generated by MCP Creator — Connect Anything
"""

import asyncio
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional
import aiohttp
from mcp.server.fastmcp import FastMCP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DAEMON_SCRIPT = os.path.join(BASE_DIR, "{p}_queue_daemon.py")
DAEMON_PORT = int(os.environ.get("{P_UPPER}_DAEMON_PORT", "{cfg["daemon_port"]}"))
DAEMON_URL = f"http://127.0.0.1:{{DAEMON_PORT}}"

mcp = FastMCP("{slug}")


async def ensure_daemon_running() -> Dict[str, Any]:
    timeout = aiohttp.ClientTimeout(total=3)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(f"{{DAEMON_URL}}/health") as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception:
            pass

    pythonw_exe = sys.executable.replace("python.exe", "pythonw.exe")
    if not os.path.exists(pythonw_exe):
        pythonw_exe = sys.executable

    if os.name == "nt":
        cmd_str = f'"{{pythonw_exe}}" "{{DAEMON_SCRIPT}}"'
        ps_cmd = (
            f"Invoke-CimMethod -ClassName Win32_Process -MethodName Create "
            f"-Arguments @{{{{CommandLine='{{cmd_str}}'; CurrentDirectory='{{BASE_DIR}}'}}}} | Out-Null"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        subprocess.Popen(
            [sys.executable, DAEMON_SCRIPT],
            cwd=BASE_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        for _ in range(25):
            await asyncio.sleep(0.5)
            try:
                async with session.get(f"{{DAEMON_URL}}/health") as resp:
                    if resp.status == 200:
                        return await resp.json()
            except Exception:
                pass

    raise RuntimeError(f"Nao foi possivel iniciar o daemon na porta {{DAEMON_PORT}}.")


async def daemon_request(method: str, path: str, payload: Optional[dict] = None, timeout_sec: float = 600.0) -> dict:
    await ensure_daemon_running()
    timeout = aiohttp.ClientTimeout(total=timeout_sec)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        url = f"{{DAEMON_URL}}{{path}}"
        if method.upper() == "GET":
            async with session.get(url) as resp:
                return await resp.json()
        else:
            async with session.post(url, json=payload or {{}}) as resp:
                return await resp.json()


@mcp.tool()
async def {p}_execute(
    prompt: str = "",
    input_path: str = "",
    output_path: str = "",
    priority: int = 100,
    workspace: str = "",
    wait: bool = True,
) -> Dict[str, Any]:
    """
    Executa uma tarefa no {cfg["name"]} via fila central unica (porta {cfg["daemon_port"]} / Chrome CDP porta {cfg["chrome_port"]}).
    Se ocorrer qualquer mudanca de seletor ou erro na UI, retorna automaticamente o pacote `diagnostics` para Auto-Healing.
    """
    payload = {{
        "prompt": prompt,
        "input_path": input_path,
        "output_path": output_path,
        "priority": priority,
        "workspace": workspace or os.getcwd(),
        "wait": wait,
    }}
    return await daemon_request("POST", "/enqueue", payload, timeout_sec=650.0 if wait else 30.0)


@mcp.tool()
async def {p}_execute_batch(
    items: List[Dict[str, Any]],
    workspace: str = "",
    wait: bool = True,
) -> Dict[str, Any]:
    """Enfileira multiplos jobs de uma so vez na fila central do {cfg["name"]}."""
    ws = workspace or os.getcwd()
    norm = [{{**dict(it), "workspace": it.get("workspace", ws)}} for it in items]
    return await daemon_request("POST", "/enqueue", {{"items": norm, "wait": wait}}, timeout_sec=1800.0 if wait else 30.0)


@mcp.tool()
async def {p}_queue_status(job_id: str = "", wait: bool = False) -> Dict[str, Any]:
    """Consulta o status da fila central (porta {cfg["daemon_port"]}) ou aguarda um `job_id` especifico."""
    if job_id.strip():
        q = "?wait=1" if wait else ""
        return await daemon_request("GET", f"/jobs/{{job_id.strip()}}{{q}}", timeout_sec=600.0 if wait else 15.0)
    return await daemon_request("GET", "/queue", timeout_sec=15.0)


@mcp.tool()
async def {p}_login_browser() -> Dict[str, Any]:
    """Abre o Chrome exclusivo do {cfg["name"]} (porta {cfg["chrome_port"]}) VISIVEL na tela para o 1o login humano."""
    return await daemon_request("POST", "/browser/login", timeout_sec=45.0)


@mcp.tool()
async def {p}_show_browser() -> Dict[str, Any]:
    """Traz imediatamente a janela do Chrome (porta {cfg["chrome_port"]}) para a tela (X=120, Y=90)."""
    return await daemon_request("POST", "/browser/show", timeout_sec=30.0)


@mcp.tool()
async def {p}_hide_browser() -> Dict[str, Any]:
    """Move imediatamente a janela do Chrome (porta {cfg["chrome_port"]}) para fora da tela (X=-2400, Y=0) e oculta da Taskbar."""
    return await daemon_request("POST", "/browser/hide", timeout_sec=30.0)


@mcp.tool()
async def {p}_quota_status() -> Dict[str, Any]:
    """Le os creditos/limites restantes em tempo real na plataforma e retorna o saldo consolidado do pool multi-contas."""
    return await daemon_request("POST", "/quota", {{"live": True}}, timeout_sec=35.0)


@mcp.tool()
async def {p}_accounts(
    action: str = "list",
    account_id: str = "",
    label: str = "",
    auto_rotate: bool = True,
    open_login: bool = True,
) -> Dict[str, Any]:
    """
    Gerencia o Pool Multi-Login (`accounts.json`) com rotacao automatica de cota:
      - action="list": Lista todas as contas e saldos
      - action="add": Cria novo perfil Chrome isolado (ex: `account_id="conta_2"`)
      - action="switch": Troca imediatamente para outra conta na porta {cfg["chrome_port"]}
      - action="login": Abre a conta informada visivel na tela para login
      - action="remove": Remove uma conta secundaria
      - action="set_auto_rotate": Ativa/desativa failover automatico quando acabar os creditos
    """
    return await daemon_request(
        "POST",
        "/accounts",
        {{
            "action": action,
            "account_id": account_id,
            "label": label,
            "auto_rotate": auto_rotate,
            "open_login": open_login,
        }},
        timeout_sec=60.0,
    )


@mcp.tool()
async def {p}_diagnose(take_screenshot: bool = True) -> Dict[str, Any]:
    """
    [AUTO-HEALING TOOL] Executa Raio-X completo da pagina ao vivo (atravessando Shadow DOMs,
    listando botoes/inputs/testids, chamadas de rede recentes e salvando screenshot).
    """
    return await daemon_request("POST", "/diagnose", {{"take_screenshot": take_screenshot}}, timeout_sec=45.0)


@mcp.tool()
async def {p}_update_selectors(updates: Dict[str, Any]) -> Dict[str, Any]:
    """[AUTO-HEALING TOOL] Atualiza `selectors.json` em tempo real sem reiniciar o navegador."""
    return await daemon_request("POST", "/selectors", updates, timeout_sec=15.0)


@mcp.tool()
async def {p}_reload_daemon() -> Dict[str, Any]:
    """[AUTO-HEALING TOOL] Recarrega `{p}api.py` e `selectors.json` em memoria sem derrubar a fila."""
    return await daemon_request("POST", "/reload", {{}}, timeout_sec=15.0)


if __name__ == "__main__":
    mcp.run()
'''
    return code


def render_tray_py(cfg: Dict[str, Any]) -> str:
    p = cfg["prefix"]
    P_UPPER = p.upper()
    code = f'''#!/usr/bin/env python3
"""
{cfg["name"]} — System Tray & Control Center Launcher (`{p}_tray.py`)
Generated by MCP Creator — Connect Anything
"""

import os
import urllib.request
import webbrowser
from PIL import Image, ImageDraw
import pystray

DAEMON_PORT = int(os.environ.get("{P_UPPER}_DAEMON_PORT", "{cfg["daemon_port"]}"))
DAEMON_URL = f"http://127.0.0.1:{{DAEMON_PORT}}"


def create_icon() -> Image.Image:
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((4, 4, 60, 60), fill=(99, 102, 241, 255), outline=(165, 180, 252, 255), width=3)
    draw.polygon([(26, 18), (26, 46), (46, 32)], fill=(255, 255, 255, 255))
    return img


def post_action(path: str):
    try:
        req = urllib.request.Request(f"{{DAEMON_URL}}{{path}}", data=b"{{}}", headers={{"Content-Type": "application/json"}}, method="POST")
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[!] Aviso ao chamar {{path}}: {{e}}")


def run_tray():
    menu = pystray.Menu(
        pystray.MenuItem("📊 Abrir Dashboard Web", lambda: webbrowser.open(f"{{DAEMON_URL}}/dashboard"), default=True),
        pystray.MenuItem("👁️ Mostrar Chrome", lambda: post_action("/browser/show")),
        pystray.MenuItem("👻 Esconder Chrome (Off-Screen)", lambda: post_action("/browser/hide")),
        pystray.MenuItem("🔑 Login Inicial", lambda: post_action("/browser/login")),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("🔄 Recarregar Seletores (Hot-Reload)", lambda: post_action("/reload")),
        pystray.MenuItem("❌ Sair do Tray", lambda icon, item: icon.stop()),
    )
    icon = pystray.Icon("{p}_mcp", create_icon(), "{cfg["name"]} MCP (:{cfg["daemon_port"]})", menu)
    icon.run()


if __name__ == "__main__":
    run_tray()
'''
    return code


def render_setup_mcp_py(cfg: Dict[str, Any]) -> str:
    p = cfg["prefix"]
    slug = cfg["slug"]
    code = f'''#!/usr/bin/env python3
"""
Universal 1-Click Installer for {cfg["name"]} (`setup_mcp.py`)
Registers the MCP server and Skill across:
  - Google Antigravity (~/.gemini/config/mcp_config.json + Skill)
  - Claude Code (~/.claude.json + .mcp.json + ~/.claude/skills/{slug}/SKILL.md)
  - Cursor (~/.cursor/mcp.json)
"""

import json
import shutil
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MCP_SERVER_SCRIPT = str(BASE_DIR / "{p}_mcp_server.py")
SKILL_SRC = BASE_DIR / "SKILL.md"
PYTHON_EXE = sys.executable


def merge_mcp_json(file_path: Path):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    data = {{}}
    if file_path.exists():
        try:
            content = file_path.read_text(encoding="utf-8").strip()
            if content:
                data = json.loads(content)
        except Exception:
            data = {{}}
    if not isinstance(data, dict):
        data = {{}}
    mcp_servers = data.setdefault("mcpServers", {{}})
    mcp_servers["{slug}"] = {{
        "command": PYTHON_EXE,
        "args": [MCP_SERVER_SCRIPT],
    }}
    file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [OK] Registered '{slug}' in: {{file_path}}")


def main():
    print("=" * 68)
    print("  ⚡ UNIVERSAL MCP INSTALLER — {cfg["name"]}")
    print("=" * 68)
    home = Path.home()
    merge_mcp_json(BASE_DIR / ".mcp.json")
    merge_mcp_json(home / ".gemini" / "config" / "mcp_config.json")
    merge_mcp_json(home / ".cursor" / "mcp.json")
    if (home / ".claude.json").exists():
        merge_mcp_json(home / ".claude.json")

    if SKILL_SRC.exists():
        for dest_dir in (
            home / ".gemini" / "config" / "skills" / "{slug}",
            home / ".claude" / "skills" / "{slug}",
        ):
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SKILL_SRC, dest_dir / "SKILL.md")
            print(f"  [OK] Skill installed in: {{dest_dir / 'SKILL.md'}}")

    print("\\n✅ Installation complete! Run `{p}_login_browser` on first use.")


if __name__ == "__main__":
    main()
'''
    return code


def render_generated_skill_md(cfg: Dict[str, Any]) -> str:
    p = cfg["prefix"]
    slug = cfg["slug"]
    return f"""---
name: {slug}
description: Conecta e automatiza o {cfg["name"]} ({cfg["url"]}) usando Chrome CDP isolado (porta {cfg["chrome_port"]}), Fila Central Única (porta {cfg["daemon_port"]}), Multi-Login com Failover de Quota, Modo Invisível Off-Screen e Protocolo Completo de Auto-Healing.
---

# ⚡ {cfg["name"]} MCP (`{slug}`)

Gerado com a arquitetura blindada do **MCP Creator — Connect Anything**.

## 🛠️ Ferramentas MCP Disponíveis
- `{p}_execute(prompt, input_path, output_path, priority, wait)`: Envia um job para a fila central única (porta `{cfg["daemon_port"]}`).
- `{p}_execute_batch(items, wait)`: Enfileira múltiplos jobs de uma só vez.
- `{p}_queue_status(job_id, wait)`: Consulta a fila central ou aguarda um `job_id`.
- `{p}_quota_status()`: Lê os créditos/limites restantes em tempo real e mostra o saldo do pool multi-contas.
- `{p}_accounts(action, account_id, label, auto_rotate)`: Gerencia o Pool Multi-Login (`list`, `add`, `switch`, `login`, `remove`, `set_auto_rotate`).
- `{p}_login_browser()` / `{p}_show_browser()` / `{p}_hide_browser()`: Controle instantâneo da janela Off-Screen do Chrome (porta `{cfg["chrome_port"]}`).
- `{p}_diagnose()` / `{p}_update_selectors(updates)` / `{p}_reload_daemon()`: Loop fechado de Auto-Healing!
"""


def render_generated_readme_md(cfg: Dict[str, Any]) -> str:
    p = cfg["prefix"]
    slug = cfg["slug"]
    return f"""# ⚡ {cfg["name"]} MCP (`{slug}`)

Servidor MCP inquebrável para **{cfg["name"]}** (`{cfg["url"]}`), gerado pelo **[MCP Creator — Connect Anything](https://github.com/NicolasCoder/mcp-creator-connect-anything)**.

## ✨ Recursos Ativos neste MCP
- **Porta CDP Isolada**: `{cfg["chrome_port"]}` | **Porta da Fila Central**: `{cfg["daemon_port"]}`
- **Modo de Visibilidade**: `{cfg["visibility"]}` (`{p}_show_browser` / `{p}_hide_browser` / `{p}_login_browser`)
- **Multi-Login & Smart Quota Rotation**: `{"Ativado" if cfg["enable_multi_login"] else "Desativado"}` (`accounts.json`)
- **Leitor de Créditos em Tempo Real**: `{"Ativado" if cfg["enable_quota_reader"] else "Desativado"}` (`{p}_quota_status`)
- **Escudo Triplo de Silêncio Absoluto**: `{"Ativado" if cfg["enable_mute_audio"] else "Desativado"}`
- **Dashboard Web Ao Vivo**: `http://127.0.0.1:{cfg["daemon_port"]}/dashboard`

## 🚀 Instalação Rápida

```bash
pip install -r requirements.txt
python setup_mcp.py
```

Para abrir o System Tray:
```bash
python {p}_tray.py
```
"""


def generate_mcp_project(cfg: Dict[str, Any]) -> Path:
    out_dir = Path(cfg["output_dir"]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "diagnostics").mkdir(exist_ok=True)
    (out_dir / "outputs").mkdir(exist_ok=True)

    p = cfg["prefix"]

    # 1. Copy or write dom_bypass.js
    if TEMPLATE_DOM_BYPASS.exists():
        shutil.copy2(TEMPLATE_DOM_BYPASS, out_dir / "dom_bypass.js")
    else:
        (out_dir / "dom_bypass.js").write_text("// dom_bypass.js\n", encoding="utf-8")

    # 2. Write JSON configs
    (out_dir / "selectors.json").write_text(render_selectors_json(cfg), encoding="utf-8")
    (out_dir / "config.json").write_text(render_config_json(cfg), encoding="utf-8")

    # 3. Write Python core modules
    (out_dir / f"{p}api.py").write_text(render_core_api_py(cfg), encoding="utf-8")
    (out_dir / f"{p}_queue_daemon.py").write_text(render_queue_daemon_py(cfg), encoding="utf-8")
    (out_dir / f"{p}_mcp_server.py").write_text(render_mcp_server_py(cfg), encoding="utf-8")
    if cfg.get("enable_tray", True):
        (out_dir / f"{p}_tray.py").write_text(render_tray_py(cfg), encoding="utf-8")
    (out_dir / "setup_mcp.py").write_text(render_setup_mcp_py(cfg), encoding="utf-8")

    # 4. Write SKILL.md, README.md, requirements.txt, .gitignore
    (out_dir / "SKILL.md").write_text(render_generated_skill_md(cfg), encoding="utf-8")
    (out_dir / "README.md").write_text(render_generated_readme_md(cfg), encoding="utf-8")
    (out_dir / "requirements.txt").write_text(
        "mcp>=1.2.0\nplaywright>=1.49.0\naiohttp>=3.10.0\npsutil>=6.0.0\npystray>=0.19.5\nPillow>=10.0.0\n",
        encoding="utf-8",
    )
    (out_dir / ".gitignore").write_text(
        "__pycache__/\n*.pyc\n*.db\ndiagnostics/*.png\ndiagnostics/*.json\noutputs/\n.env\n",
        encoding="utf-8",
    )

    return out_dir


def parse_args():
    parser = argparse.ArgumentParser(
        description="⚡ MCP Creator — Connect Anything: Scaffold an unbreakable, self-healing Web-to-MCP Server."
    )
    parser.add_argument("--name", default="Custom Web Studio", help="Human-readable name of the target web service")
    parser.add_argument("--prefix", default="", help="Short prefix for MCP tool names (e.g. 'suno', 'eleven', 'heygen')")
    parser.add_argument("--url", default="https://example.com/app", help="Target URL of the web application")
    parser.add_argument("--output-dir", default="", help="Destination directory for the generated MCP project")
    parser.add_argument("--chrome-port", type=int, default=9363, help="Isolated Chrome CDP port (default: 9363)")
    parser.add_argument("--daemon-port", type=int, default=9364, help="Central Queue Daemon HTTP port (default: 9364)")
    parser.add_argument(
        "--visibility",
        choices=["offscreen", "visible", "hybrid"],
        default="offscreen",
        help="Browser visibility mode (default: offscreen)",
    )
    parser.add_argument("--tray", dest="enable_tray", action="store_true", default=True, help="Generate System Tray app")
    parser.add_argument("--no-tray", dest="enable_tray", action="store_false", help="Disable System Tray app")
    parser.add_argument("--dashboard", dest="enable_dashboard", action="store_true", default=True, help="Enable live Web Dashboard")
    parser.add_argument("--multi-login", dest="enable_multi_login", action="store_true", default=True, help="Enable Multi-Account Pool & failover")
    parser.add_argument("--no-multi-login", dest="enable_multi_login", action="store_false", help="Disable Multi-Account Pool")
    parser.add_argument("--quota-reader", dest="enable_quota_reader", action="store_true", default=True, help="Enable real-time quota/credits reader")
    parser.add_argument("--quota-unit", default="credits", help="Quota unit name (e.g. credits, minutes, tokens)")
    parser.add_argument("--mute-audio", dest="enable_mute_audio", action="store_true", default=True, help="Enable Triple Audio Silence Shield")
    parser.add_argument("--no-mute-audio", dest="enable_mute_audio", action="store_false", help="Allow browser audio")
    parser.add_argument("--auto-healing", dest="enable_auto_healing", action="store_true", default=True, help="Enable Self-Healing tools")
    parser.add_argument("--non-interactive", action="store_true", help="Skip interactive prompts and use CLI flags directly")
    return parser.parse_args()


def main():
    args = parse_args()
    prefix = slugify(args.prefix or args.name, "_")
    slug_base = slugify(args.name, "-")
    slug = f"{slug_base}-mcp" if not slug_base.endswith("-mcp") else slug_base

    defaults = {
        "name": args.name,
        "slug": slug,
        "prefix": prefix,
        "url": args.url,
        "chrome_port": args.chrome_port,
        "daemon_port": args.daemon_port,
        "visibility": args.visibility,
        "enable_tray": args.enable_tray,
        "enable_dashboard": args.enable_dashboard,
        "enable_multi_login": args.enable_multi_login,
        "enable_quota_reader": args.enable_quota_reader,
        "quota_unit": args.quota_unit,
        "enable_mute_audio": args.enable_mute_audio,
        "enable_auto_healing": args.enable_auto_healing,
        "output_dir": args.output_dir or str(Path.cwd() / slug),
    }

    if args.non_interactive or not sys.stdin.isatty():
        cfg = defaults
    else:
        cfg = run_interactive_wizard(defaults)

    out_dir = generate_mcp_project(cfg)
    p = cfg["prefix"]
    print("\n" + "=" * 74)
    print(f"✅ MCP GERADO COM SUCESSO: {cfg['name']} ({cfg['slug']})")
    print("=" * 74)
    print(f"📁 Diretório        : {out_dir}")
    print(f"🌐 URL Alvo         : {cfg['url']}")
    print(f"🔌 Chrome CDP Port  : {cfg['chrome_port']} | Fila Daemon Port: {cfg['daemon_port']}")
    print(f"👻 Visibilidade     : {cfg['visibility']} | Silêncio Triplo: {cfg['enable_mute_audio']}")
    print(f"👥 Multi-Login Pool : {cfg['enable_multi_login']} | Quota Reader: {cfg['enable_quota_reader']} ({cfg['quota_unit']})")
    print(f"🛠️  Arquivos Criados :")
    print(f"   - {p}_mcp_server.py   (11 tools MCP prontas c/ Auto-Healing)")
    print(f"   - {p}_queue_daemon.py (Fila SQLite + Multi-Login + Dashboard em http://127.0.0.1:{cfg['daemon_port']}/dashboard)")
    print(f"   - {p}api.py           (Motor CDP Off-Screen + Triple-Capture + Quota Failover)")
    print(f"   - dom_bypass.js       (Shadow-DOM Piercing + React Fiber Setter + Silence Shield)")
    if cfg.get("enable_tray"):
        print(f"   - {p}_tray.py         (System Tray Icon & Quick Actions)")
    print(f"   - selectors.json      (Seletores em cascata auto-curáveis)")
    print(f"   - setup_mcp.py        (Instalador 1-Click para Claude, Cursor e Antigravity)")
    print("=" * 74)


if __name__ == "__main__":
    main()
