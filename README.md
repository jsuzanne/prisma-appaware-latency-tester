═══════════════════════════════════════════════════════════════════
text
# Prisma AppAware Latency Tester

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Prisma SD-WAN](https://img.shields.io/badge/Prisma-SD--WAN-orange.svg)

**Demonstrate Prisma SD-WAN's Layer 7 intelligence for latency troubleshooting**

Showcase Prisma SD-WAN's unique ability to **differentiate network latency from server/application latency** - a key differentiator for instant root cause identification.

---

## 🏗️ Architecture

### Real-World Scenario

Branch Office (Remote) WAN/SD-WAN Data Center
────────────────────── ────────── ────────────

Ubuntu207 (CLIENT) Prisma Ubuntu201 (SERVER)

End users Monitors - Applications

Workstations Here! ◄─ - Databases

Business hours 8h-18h - Slow processing
- Backend APIs

text
 │                                          │
 └────────── Internet/MPLS ─────────────────┘
text

**CLIENT (Ubuntu207)** = Branch office users  
**SERVER (Ubuntu201)** = Datacenter applications (slow CRM, ERP, databases)  
**PRISMA SD-WAN** = Measures network vs server latency separately

---

## 🎯 The Problem This Solves

**Customer Pain:**
> "Users complain the CRM is slow. Is it the network or the server?"

**Without Prisma** 😕:
- See only: Total time = 8.2 seconds
- Result: Hours of finger-pointing between network and server teams

**With Prisma** 😎:
- Network RTT: **15 ms** ✓ (healthy)
- Server Response: **8.1 sec** ⚠ (problem!)
- Result: **Instant identification** → engage application team

---

## 📊 Features

### Server (Ubuntu201 - Datacenter)
- Simulates slow applications (5-10 second processing)
- Configurable delay and data size
- Multi-client support
- Systemd service

### Client (Ubuntu207 - Branch)
- Business hours emulation (8h-18h weekdays)
- Peak hour simulation (10h, 14h, 16h)
- Off-hours minimal activity
- Multiple server support

### Traffic Patterns

| Time Period | Interval | Activity |
|-------------|----------|----------|
| Business hours (8h-18h) | 3 min | Normal |
| Peak hours | 1.5 min | High |
| Night (18h-8h) | 10-30 min | Minimal |
| Weekend | 30-60 min | Very low |

---

## 🚀 Quick Start

### Server Installation (Ubuntu201 - Datacenter)

git clone https://github.com/jsuzanne/prisma-appaware-latency-tester.git
cd prisma-appaware-latency-tester
chmod +x install-server.sh
sudo ./install-server.sh
sudo systemctl start tcp-server
sudo systemctl enable tcp-server

text

### Client Installation (Ubuntu207 - Branch)

git clone https://github.com/jsuzanne/prisma-appaware-latency-tester.git
cd prisma-appaware-latency-tester
chmod +x install-client.sh
sudo ./install-client.sh

Configure server IP
sudo nano /opt/tcp-client/server01.env

Set: HOST=192.168.1.201 and PORT=18890
sudo systemctl start tcp-client@server01
sudo systemctl enable tcp-client@server01

text

### View Logs

Server logs (Ubuntu201)
sudo journalctl -u tcp-server -f

Client logs (Ubuntu207)
sudo journalctl -u tcp-client@server01 -f

text

---

## 📖 Example Output

### Client Output (Branch)
[CLIENT] Transaction #42 - Semaine - Heures de travail
[CLIENT] Connexion à 192.168.1.201:18890...
[CLIENT] Connecté en 0.012 secondes ← Network latency
[CLIENT] Temps de transaction: 12.45 secondes ← Total time
[CLIENT] Débit: 8.03 Mo/s

text

### What Prisma Shows

Application Performance Dashboard
├─ Network RTT: 12 ms ✓ Healthy
├─ Server Response: 8.2 sec ⚠ Slow
├─ Data Transfer: 4.2 sec ✓ Good
└─ Root Cause: Server Processing Delay

text

---

## ⚙️ Configuration

### Server Settings

sudo nano /etc/systemd/system/tcp-server.service

Adjust these parameters:
--delay-min 5 # Min processing delay (seconds)
--delay-max 10 # Max processing delay (seconds)
--data-size 104857600 # Payload size (100 MB)

text

### Multiple Servers (Client)

Configure second server
sudo nano /opt/tcp-client/server02.env
HOST=192.168.1.202
PORT=18890

Start it
sudo systemctl start tcp-client@server02
sudo systemctl enable tcp-client@server02

text

---

## 🎬 Demo Usage

Perfect for:
- **SD-WAN Demos**: Showcase Layer 7 intelligence
- **Customer POCs**: Prove troubleshooting value
- **Training**: Teach network vs app latency
- **Testing**: Validate SD-WAN policies

See [Demo Script](docs/DEMO.md) for step-by-step demo guide.

---

## 🔍 Troubleshooting

### Client can't connect

Test connectivity
ping 192.168.1.201
nc -zv 192.168.1.201 18890

Check firewall
sudo ufw allow 18890/tcp

text

### Server not responding

sudo systemctl status tcp-server
sudo journalctl -u tcp-server -n 50
sudo netstat -tlnp | grep 18890

text

---

## 🔄 Updating

cd prisma-appaware-latency-tester
git pull origin main

Update client
sudo cp client/client.py /opt/tcp-client/
sudo systemctl restart tcp-client@*

Update server
sudo cp server/server.py /opt/tcp-server/
sudo systemctl restart tcp-server

text

---

## 🗑️ Uninstallation

### Client
sudo systemctl stop tcp-client@*
sudo systemctl disable tcp-client@*
sudo rm -rf /opt/tcp-client
sudo rm /etc/systemd/system/tcp-client@.service
sudo systemctl daemon-reload

text

### Server
sudo systemctl stop tcp-server
sudo systemctl disable tcp-server
sudo rm -rf /opt/tcp-server
sudo rm /etc/systemd/system/tcp-server.service
sudo systemctl daemon-reload

text

---

## 📚 Documentation

- **[Demo Script](docs/DEMO.md)** - Complete demo walkthrough
- **[Configuration](docs/CONFIGURATION.md)** - Advanced settings

---

## 🤝 Contributing

Contributions welcome! Open an issue or submit a pull request.

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 📧 Support

- **Issues**: https://github.com/jsuzanne/prisma-appaware-latency-tester/issues
- **Author**: Julien Suzanne - Palo Alto Networks SASE Specialist
- **LinkedIn**: [Connect](https://www.linkedin.com/in/julien-suzanne/)

---

**Made with ❤️ for Prisma SD-WAN SEs and Partners**

*Stop blaming the network when it's the server* 🚀
text
═══════════════════════════════════════════════════════════════════
