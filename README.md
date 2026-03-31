# Hygiene-Core

<div align="center">
  <img alt="Arch Linux" src="https://img.shields.io/badge/Arch_Linux-Optimization-000000?style=for-the-badge&logo=arch-linux&logoColor=1793D1">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-000000?style=for-the-badge&logo=python&logoColor=00FF4E">
  <img alt="Systemd" src="https://img.shields.io/badge/Systemd-Automated-000000?style=for-the-badge&logo=linux&logoColor=00FF4E">
  <br>
  <img alt="License" src="https://img.shields.io/badge/License-MIT-000000?style=for-the-badge">
  <img alt="Open Source" src="https://img.shields.io/badge/Open_Source-❤️-000000?style=for-the-badge">
  <br>
  <img alt="Telegram" src="https://img.shields.io/badge/Telegram-Notifications-000000?style=for-the-badge&logo=telegram&logoColor=blue">
</div>

<br>

<div align="center">
  <img alt="Hygiene-Core Banner" src="https://github.com/user-attachments/assets/457f0f48-71e5-477e-a24d-1b65545f4f49" width="800">
</div>

<br>

<p align="center">
  <a href="#english">🇺🇸 EN</a> | <a href="#turkish">🇹🇷 TR</a>
</p>

<a name="english"></a>

## 🇺🇸 EN

### ⚙️ System Architecture

```mermaid
graph LR
    subgraph Automation
        T[Systemd Timer] --> S[Systemd Service]
    end
    subgraph Core Engine
        S --> O[Orchestrator]
        O --> M1[Cache Cleaner]
        O --> M2[Custom Modules...]
    end
    subgraph Reporting
        M1 & M2 --> R[Result Parser]
        R --> TL[Telegram Bot]
    end
```

**Hygiene-Core** is a modular, lightweight maintenance engine designed for Arch Linux. It automates manual cleanup tasks, optimizes system storage, and sends aesthetic reports via Telegram.

<div align="left">
  <img src="https://github.com/user-attachments/assets/38873e99-e3a2-48b2-b8ec-587d4b71ae89" width="800" alt="Telegram Report Example">
</div>

#### ✨ Features

- **Modular Design:** Each task is an independent plugin in `modules/`.
- **Telegram Integration:** Instant reporting of cleaned space.
- **Safety First:** Includes `Dry Run` mode and `lsof` checks to protect active files.
- **Idle Execution:** Runs via Systemd with idle priority to ensure zero UX impact.

#### 🛡️ Dry Run Mode

By default, Hygiene-Core is shipped with `dry_run: true` in `config.yaml`. In this mode, the engine will scan the system, calculate the potential clean up size, and send the Telegram report, **but it will not permanently delete any files**.
To execute the actual cleanup process, edit the configuration:

```yaml
# config.yaml
dry_run: false
```

#### 🚀 Quick Start

```bash
git clone [https://github.com/cybalp/Hygiene-Core](https://github.com/cybalp/Hygiene-Core)
cd Hygiene-Core
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env # Add your Telegram credentials
```

## 🛠 Module Writing Guide

Add a `.py` file to `modules/`. The orchestrator will auto-discover it.

```python
class MyCustomModule:
    def __init__(self, config):
        self.config = config
    def run(self):
        return {"module": "Name", "status": "Success", "cleaned_mb": 10.0}
```

---

## 🇹🇷 TR

### ⚙️ Sistem Mimarisi

**Hygiene-Core**, Arch Linux sistemleri için tasarlanmış, modüler ve hafif bir bakım motorudur. Manuel temizlik işlerini otomatize eder, depolamayı optimize eder ve sonuçları Telegram üzerinden raporlar.

<div align="left">
  <img src="https://github.com/user-attachments/assets/38873e99-e3a2-48b2-b8ec-587d4b71ae89" width="800" alt="Telegram Report Example">
</div>

#### ✨ Özellikler

- **Modüler Tasarım:** Her temizlik görevi `modules/` altında bağımsız bir eklentidir.
- **Telegram Entegrasyonu:** Temizlenen alan miktarını anında raporlar.
- **Güvenlik:** `Dry Run` modu ve `lsof` kontrolü ile aktif dosyaları korur.
- **Düşük Öncelikli Çalışma:** Systemd üzerinden `idle` modunda çalışarak sistem performansını etkilemez.

#### 🛡️ Dry Run Modu

Varsayılan olarak Hygiene-Core, `config.yaml` dosyasında `dry_run: true` korumasıyla gelir. Bu modda sistem taranır, potansiyel olarak silinebilecek dosya boyutu hesaplanır ve Telegram'a rapor gönderilir, **ancak hiçbir dosya fiziksel olarak silinmez**.
Sistemi gerçekten temizlemek (silme işlemlerini onaylamak) için yapılandırmayı değiştirin:

```yaml
# config.yaml
dry_run: false
```

<a name="turkish"></a>

#### 🚀 Hızlı Başlangıç

```bash
git clone [https://github.com/cybalp/Hygiene-Core](https://github.com/cybalp/Hygiene-Core)
cd Hygiene-Core
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env # Telegram bilgilerini girin
```

---

## 🛠 Modül Yazım Kılavuzu

`modules/` dizinine bir `.py` dosyası ekleyin. Orchestrator onu otomatik olarak keşfedecektir.

```python
class MyCustomModule:
    def __init__(self, config):
        self.config = config
    def run(self):
        return {"module": "Name", "status": "Success", "cleaned_mb": 10.0}
```

---

<!--SUPPORTS-->

<h1 align="center">ꜱᴜᴘᴘᴏʀᴛꜱ ᴍᴇ ∞ ♡</h1>
<p align="center">
  <a href="https://github.com/sponsors/cybalp"><img src="https://img.shields.io/badge/Sponsor-GitHub-00FF4E?style=for-the-badge&logo=github-sponsors&labelColor=000000&logoColor=00FF4E" alt="Sponsor"></a>
</p>
<p align="center">
<a href="https://www.buymeacoffee.com/cybalpxb"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee"></a>
</p>
<br>
<p align="center">
  <img src="https://cybalp.me/assets/qr-codes/usdt.png" width="100">
  <br>
  <code align="center">TKPTZj988cNC8vPwcexPz8mfrCzYtT7Gkq</code>
  <p align="center">USDT (TRC20)</p>
</p>
