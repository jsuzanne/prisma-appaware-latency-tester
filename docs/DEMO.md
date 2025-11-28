# Demo Script - Prisma AppAware Latency Tester

## 🎯 Objective

Demonstrate how Prisma SD-WAN's Layer 7 intelligence **differentiates network latency from server latency** for instant root cause identification.

**Duration**: 10 minutes

---

## 📋 Pre-Demo Setup (5 minutes)

### 1. Verify Server (Ubuntu201 - Datacenter)

ssh ubuntu201
sudo systemctl status tcp-server
sudo journalctl -u tcp-server -n 5

text

Expected:
● tcp-server.service - active (running)
[SERVEUR] Démarré sur 0.0.0.0:18890
[SERVEUR] Délai de réponse: 5-10 secondes

text

### 2. Verify Client (Ubuntu207 - Branch)

ssh Ubuntu207
sudo systemctl status tcp-client@server01
sudo journalctl -u tcp-client@server01 -n 10

text

Expected:
[CLIENT] Transaction #XX - Semaine - Heures de travail
[CLIENT] Connecté en 0.015 secondes
[CLIENT] Temps de transaction: 12.34 secondes

text

### 3. Open Prisma Dashboard

- Login to Prisma SD-WAN
- Navigate to: **Monitor → Applications**
- Filter: Port 18890
- Keep open on second screen

---

## 🎭 Demo Flow

### PART 1: Set the Scene (2 min)

**YOU SAY:**
> "Imagine it's Monday morning. You get a ticket:
> 
> *'Users at the Paris branch say the CRM is extremely slow. 10+ seconds response time. Please check the network immediately.'*
>
> What do you normally do?"

**CUSTOMER SAYS:**
> "Check ping, bandwidth, traceroute..."

**YOU SAY:**
> "Exactly. Hours of troubleshooting. Network blames server. Server blames network. Sound familiar? Let me show you a better way..."

---

### PART 2: Show the Traffic (1 min)

sudo journalctl -u tcp-client@server01 -f

text

**YOU SAY:**
> "Here's our branch user making requests to the datacenter application. Watch these numbers..."

**Point out:**
- `Connecté en 0.015 secondes` ← Network connection
- `Temps de transaction: 12.34 secondes` ← Total time
- `Débit: 8.03 Mo/s` ← Throughput

**YOU SAY:**
> "12 seconds total. But WHERE is the delay? Network or server? Let's look at Prisma..."

---

### PART 3: The Magic - Prisma Dashboard (3 min)

**Switch to Prisma Dashboard**

**Point to metrics:**
Application Performance
├─ Network RTT: 15 ms ✓ Green
├─ Server Response: 8.2 sec ⚠ Red
├─ Data Transfer: 4.1 sec ✓ Green
└─ Total Transaction: 12.3 sec

text

**YOU SAY:**
> "Look at this breakdown:
> - **Network**: 15 milliseconds. Perfect!
> - **Server**: 8.2 seconds processing. That's the problem!
> - **Transfer**: 4 seconds. Bandwidth is fine.
>
> **The network is healthy. The server is slow.**
>
> Legacy SD-WAN shows '12 seconds total' and you waste hours checking the network.
>
> Prisma shows the root cause instantly. Engage the application team immediately.
>
> We just saved 6+ hours of troubleshooting."

---

### PART 4: Business Hours Intelligence (2 min)

**Show logs:**

sudo journalctl -u tcp-client@server01 -n 20

text

**Point out:**
[CLIENT] - Semaine - Heures de travail ← Business hours
[CLIENT] Attente de 120 secondes ← Active (2 min)

[CLIENT] - Semaine - Hors heures ← Night
[CLIENT] Attente de 1200 secondes ← Minimal (20 min)

text

**YOU SAY:**
> "The client simulates real user behavior:
> - **Business hours**: Active every 2-3 minutes
> - **Night**: Minimal (every 20 minutes)
> - **Weekend**: Very low (every 45 minutes)
>
> This creates realistic traffic patterns for your demos and testing."

---

### PART 5: The Value (2 min)

**YOU SAY:**
> "Let me show you the business impact..."

**Show comparison:**

Traditional SD-WAN:
──────────────────
User complains (9:00 AM)
Network troubleshooting (11:00 AM)
"Network is fine" (12:00 PM)
Escalate to servers (1:00 PM)
Issue identified (4:00 PM)
──────────────────────────────────
MTTR: 7 hours

Prisma SD-WAN:
──────────────
User complains (9:00 AM)
Check Prisma (9:02 AM)
See: Server=8s, Net=15ms (9:02 AM)
Engage server team (9:05 AM)
──────────────────────────────────
MTTR: 5 minutes

text

**YOU SAY:**
> "That's **84x faster**. This means:
> - Reduced downtime
> - No finger-pointing
> - Better user experience
> - Lower operational costs
>
> And this is just ONE application. Imagine this visibility across Salesforce, Office 365, SAP, everything..."

---

## 🎬 Closing

**YOU SAY:**
> "This demo tool is open source on GitHub. You can deploy it in your lab today to test Prisma's Layer 7 capabilities.
>
> Questions?"

---

## 📊 Expected Q&A

**Q: "Does this work with HTTPS?"**
A: "Yes! Prisma uses SSL inspection. We can also use SNI for basic app ID without decryption."

**Q: "Can we see this for real apps like Salesforce?"**
A: "Absolutely! This demo uses custom TCP for clarity, but Prisma provides the same visibility for 5,000+ pre-defined apps."

**Q: "What if the network IS the problem?"**
A: "Great question! Then you'd see high Network RTT but low Server Response, instantly identifying a WAN issue."

**Q: "What's the overhead of Layer 7 inspection?"**
A: "Minimal. Hardware-accelerated DPI adds typically <1ms. The visibility gained far outweighs any overhead."

---

## 🔧 Demo Variations

### Show Network Problem

Add packet loss on Ubuntu207
sudo tc qdisc add dev eth0 root netem loss 5% delay 100ms

Now Prisma shows both network AND server issues
text

### Show Fast Application

On Ubuntu201
sudo nano /etc/systemd/system/tcp-server.service

Change: --delay-min 0.5 --delay-max 1
sudo systemctl restart tcp-server

Now everything is green!
text

---

**🎯 Success Criteria:**
- ✅ Customer understands Layer 7 value
- ✅ Customer sees instant root cause benefit
- ✅ Customer requests POC
- ✅ Customer shares with team

**Good luck!** 🚀

