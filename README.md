# Prisma App-Aware Latency Tester

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

A TCP-based latency measurement tool designed to demonstrate **Prisma SD-WAN's Layer 7 intelligence** in differentiating network latency from application server latency.

## 🎯 Purpose

Traditional network monitoring tools can only see end-to-end latency. When applications are slow, teams waste time debating: **Is it the network or the server?**

**Prisma SD-WAN's Layer 7 visibility solves this** by measuring:
- **Network RTT** (Round-Trip Time)
- **Server Processing Time**
- **Total Transaction Time**

This tool simulates realistic application behavior to showcase Prisma SD-WAN's troubleshooting capabilities.

---

## 🏗️ Architecture

Branch Site (Remote) → Datacenter (Central)
────────────────────── ────────────────────
Ubuntu Client Ubuntu Server

Simulates users - Hosts applications

Outbound traffic - Slow backend

Business hours patterns - Database queries
- Processing delays

   │                                      │
   └──────── WAN / SD-WAN ───────────────┘

---

## 📦 Features

- **Business Hours Emulation**: Server introduces 5-10s delay during 8 AM - 6 PM to simulate peak load
- **Transaction-Based Testing**: Each connection sends request, receives 1MB response, then closes
- **Automatic Reconnection**: Client establishes new TCP session every 3 seconds
- **Systemd Integration**: Runs as persistent background service
- **Multi-Instance Support**: Test multiple servers simultaneously from one client

---

## 🚀 Quick Start

### Installation

#### Server Side (Datacenter)

Clone repository
```bash
git clone https://github.com/jsuzanne/prisma-appaware-latency-tester.git
cd prisma-appaware-latency-tester
```

Run installation script
```bash
sudo ./install-server.sh
```

Verify service
```bash
sudo systemctl status tcp-server
sudo journalctl -u tcp-server -f
```

#### Client Side (Branch Site)

Clone repository
```bash
git clone https://github.com/jsuzanne/prisma-appaware-latency-tester.git
cd prisma-appaware-latency-tester
```

Run installation script
```bash
sudo ./install-client.sh
```

Configure target server
```bash
sudo nano /opt/tcp-client/server01.env
```

Edit `server01.env`:
```bash
HOST=<server-ip-address>
PORT=18890
```

Enable and start:
```bash
sudo systemctl enable tcp-client@server01
sudo systemctl start tcp-client@server01
```
sudo systemctl status tcp-client@server01

---

## 📊 Usage

### Starting Services

**Server:**
```bash
sudo systemctl start tcp-server
```

**Client (single instance):**
```bash
sudo systemctl start tcp-client@server01
```

**Client (multiple servers):**
Create additional .env files
```bash
sudo cp /opt/tcp-client/server01.env /opt/tcp-client/server02.env
sudo nano /opt/tcp-client/server02.env # Edit with different HOST/PORT
```

Start multiple instances
```bash
sudo systemctl start tcp-client@server01
sudo systemctl start tcp-client@server02
sudo systemctl enable tcp-client@server01 # Auto-start on boot
```

### Monitoring

**Live logs:**
Server logs
```bash
sudo journalctl -u tcp-server -f
```

Client logs (specific instance)
```bash
sudo journalctl -u tcp-client@server01 -f
```

Client logs (all instances)
```bash
sudo journalctl -u 'tcp-client@*' -f
```

**Recent logs:**
```bash
sudo journalctl -u tcp-server -n 100
sudo journalctl -u tcp-client@server01 -n 100
```

---

## 🔧 Configuration

### Server Configuration

Edit `/opt/tcp-server/server.py` to adjust:
```bash
- `PORT`: Listening port (default: 18890)
- `BUSINESS_HOURS_DELAY`: Response delay range during peak (default: 5-10s)
- `BUSINESS_HOURS`: Time window for slow responses (default: 8-18)
- `RESPONSE_SIZE`: Data payload size (default: 1MB)
```

### Client Configuration

Each client instance uses an environment file in `/opt/tcp-client/<instance>.env`:

```bash
HOST=192.168.1.100 # Target server IP
PORT=18890 # Target server port
```

Edit `/opt/tcp-client/client.py` to adjust:
```bash
- `--interval`: Seconds between transactions (default: 3)
```

---

## 📈 What You'll See in Prisma SD-WAN

When monitoring this traffic through Prisma SD-WAN:

**Network Metrics:**
```bash
- RTT: ~10-50ms (depends on WAN link)
- Jitter: Minimal
- Packet Loss: 0%
```

**Application Metrics:**
```bash
- Server Response Time: 5-10s (business hours) or <1s (off-hours)
- Total Transaction Time: RTT + Server Time
- Layer 7 visibility shows exact breakdown
```

**Key Insight:** When users complain about slowness during business hours, Prisma SD-WAN immediately shows **server processing (8s) vs network (20ms)** - no guesswork!

---

## 🛠️ Troubleshooting

**Service won't start:**
```bash
sudo systemctl status tcp-server # Check error details
sudo journalctl -xe # View full system logs
```
**Client can't connect:**
Verify server is listening
```bash
sudo netstat -tlnp | grep 18890
```

Test connectivity
```bash
telnet <server-ip> 18890
```

Check firewall
```bash
sudo ufw status
sudo ufw allow 18890/tcp
```

**Logs not showing:**
Verify service is running
```bash
systemctl is-active tcp-server
systemctl is-active tcp-client@server01
```

Check journal size
```bash
journalctl --disk-usage
```

---

## 📋 File Structure

```text
prisma-appaware-latency-tester/
├── README.md
├── LICENSE
├── install-server.sh # Server installation script
├── install-client.sh # Client installation script
├── client/
│ ├── client.py # Client script
│ └── tcp-client@.service # Systemd template service
├── server/
│ ├── server.py # Server script
│ └── tcp-server.service # Systemd service
├── config/
│ └── server01.env.example # Example environment file
└── docs/
└── DEMO.md # Demo presentation guide
```

---

## 🎤 Demo Scenario

See [docs/DEMO.md](docs/DEMO.md) for a complete presentation script including:
- Architecture explanation
- Live troubleshooting scenario
- Prisma SD-WAN dashboard walkthrough
- Q&A preparation

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues
- Submit pull requests
- Suggest improvements

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🔗 Related Resources

- [Prisma SD-WAN Documentation](https://docs.paloaltonetworks.com/prisma/prisma-sd-wan)
- [App-Aware Routing](https://docs.paloaltonetworks.com/prisma/prisma-sd-wan/prisma-sd-wan-admin/prisma-sd-wan-application-policies)
- [Layer 7 Visibility](https://docs.paloaltonetworks.com/prisma/prisma-sd-wan/prisma-sd-wan-admin/monitor-and-troubleshoot)

---

**Built for Prisma SD-WAN SEs and Partners** 🚀

