# Ableton MCP - Personal Backup

This is a personal backup of the Ableton MCP (Model Context Protocol) server with additional tools for NFL mix production.

## 🎯 What's Included

### Core MCP Components
- **MCP_Server/**: The main MCP server that communicates with Cline
- **RemoteScript/**: Ableton Live Remote Script for direct DAW control
- **AbletonMCP_Remote_Script/**: Legacy remote script files

### Production Tools (`tools/` directory)
- **mix_chopper.py**: Automatically slice audio mixes based on timestamps
- **segment_exporter.py**: Export individual segments from audio files
- **NFL_Ableton_Workflow.md**: Complete workflow guide for NFL-precision timing
- **Manual_MCP_Installation.md**: Step-by-step installation instructions
- **install_mcp.sh**: Automated installation script

## 🚀 Quick Setup

1. **Install the Remote Script**:
   ```bash
   cd tools/
   ./install_mcp.sh
   ```

2. **Configure in Ableton Live**:
   - Go to Live → Preferences → Link, Tempo & MIDI
   - Set Control Surface to "AbletonMCP"
   - Set Input/Output to any MIDI port
   - Restart Ableton Live

3. **Start the MCP Server**:
   ```bash
   source .venv/bin/activate
   python MCP_Server/server.py
   ```

## 🎵 NFL Production Workflow

For NFL halftime show production with exact timing requirements:

1. Use `mix_chopper.py` to create initial segments
2. Follow `NFL_Ableton_Workflow.md` for precision editing
3. Use MCP tools for automated Ableton control

## 📁 File Structure

```
ableton-mcp-backup/
├── MCP_Server/          # Main MCP server
├── RemoteScript/        # Ableton Remote Script
├── tools/              # Production tools
│   ├── mix_chopper.py
│   ├── segment_exporter.py
│   ├── NFL_Ableton_Workflow.md
│   └── install_mcp.sh
├── .venv/              # Python virtual environment
└── README_BACKUP.md    # This file
```

## 🔧 Requirements

- Python 3.9+
- Ableton Live 12
- pydub (for audio processing)
- ffmpeg (for audio format support)

## 📝 Notes

- Original MCP server by ahujasid
- Enhanced with NFL production tools
- Backup created: August 2025
- For NFL halftime show production workflow

## 🏈 NFL Success Metrics

- ✅ Exact timing achieved (7:00.000, 3:00.000, 2:30.000)
- ✅ Professional broadcast quality
- ✅ Zero tolerance for timing errors
- ✅ Smooth, beat-matched transitions
