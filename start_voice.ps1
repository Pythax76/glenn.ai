#!/bin/bash
# Glenn.AI Voice Assistant Launcher for PowerShell

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    🎤 Glenn.AI Voice Assistant" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Activating Glenn's voice shell..." -ForegroundColor Green
Write-Host ""

# Run the voice command
& "C:/Users/jlawrence/OneDrive - Photronics/AI/Users/Glenn/.venv/Scripts/python.exe" command_interface.py voice

Write-Host ""
Write-Host "Voice assistant session ended." -ForegroundColor Yellow
Read-Host "Press Enter to continue"
