#!/bin/bash
set -e

echo "======================================================="
echo "  Prisma AppAware Latency Tester - Client Installation"
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
mkdir -p /opt/tcp-client

echo "📄 Installing client script..."
cp client/client.py /opt/tcp-client/
chmod +x /opt/tcp-client/client.py

echo "🔧 Installing systemd service template..."
cp client/tcp-client@.service /etc/systemd/system/
systemctl daemon-reload

echo "📝 Creating example configuration..."
cat > /opt/tcp-client/server01.env << 'EOFENV'
# Configuration for server01
HOST=192.168.1.201
PORT=18890
EOFENV

echo ""
echo "✅ Client installation complete!"
echo ""
echo "=================================================="
echo "           Next Steps"
echo "=================================================="
echo ""
echo "1️⃣  Configure server connection:"
echo "   sudo nano /opt/tcp-client/server01.env"
echo "   Set HOST=<server-ip> and PORT=18890"
echo ""
echo "2️⃣  Start the client:"
echo "   sudo systemctl start tcp-client@server01"
echo ""
echo "3️⃣  Enable auto-start on boot:"
echo "   sudo systemctl enable tcp-client@server01"
echo ""
echo "4️⃣  View logs:"
echo "   sudo journalctl -u tcp-client@server01 -f"
echo ""
echo "💡 To test multiple servers, create server02.env, server03.env, etc."
echo "   Then start with: systemctl start tcp-client@server02"
echo ""
echo "=================================================="
echo ""
text
