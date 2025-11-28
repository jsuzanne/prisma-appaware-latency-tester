#!/bin/bash
set -e

echo "======================================================="
echo "  Prisma AppAware Latency Tester - Server Installation"
echo "======================================================="
echo ""

if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)"
   exit 1
fi

echo "📦 Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || {
    echo "Installing Python3..."
    apt-get update
    apt-get install -y python3
}

echo "📁 Creating directories..."
mkdir -p /opt/tcp-server

echo "📄 Installing server script..."
cp server/server.py /opt/tcp-server/
chmod +x /opt/tcp-server/server.py

echo "🔧 Installing systemd service..."
cp server/tcp-server.service /etc/systemd/system/
systemctl daemon-reload

echo ""
echo "✅ Server installation complete!"
echo ""
echo "=================================================="
echo "           Next Steps"
echo "=================================================="
echo ""
echo "1️⃣  Configure delay and data size (optional):"
echo "   sudo nano /etc/systemd/system/tcp-server.service"
echo ""
echo "2️⃣  Start the server:"
echo "   sudo systemctl start tcp-server"
echo ""
echo "3️⃣  Enable auto-start on boot:"
echo "   sudo systemctl enable tcp-server"
echo ""
echo "4️⃣  View logs:"
echo "   sudo journalctl -u tcp-server -f"
echo ""
echo "5️⃣  Open firewall (if needed):"
echo "   sudo ufw allow 18890/tcp"
echo ""
echo "=================================================="
echo ""
text
