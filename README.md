# Research---Eliminating-Credential-Stuffing-Attack-Surfaces
Eliminating Credential Stuffing Attack Surfaces: A Comparative Analysis of OAuth 2.0 and Password-Based Authentication

# OAuth 2.0 vs Traditional Authentication: Credential Stuffing Defense Analysis

## Overview
This repository contains all code, data, and configuration files for the research paper "Eliminating Credential Stuffing Attack Surfaces: A Comparative Analysis of OAuth 2.0 and Password-Based Authentication."

## Citation
If you use this code or data, please cite:
Kumar, H. (2026). Eliminating Credential Stuffing Attack Surfaces: A Comparative Analysis of OAuth 2.0 and Password-Based Authentication. [Journal Name], [Volume], [Pages]. DOI: [paper DOI]

## Repository Structure
See above directory tree.

## System Requirements
- Node.js 16+ (tested on v24.11.0)
- Python 3.8+ (tested on v3.11.0)
- MongoDB 4.4+ (tested on v8.2.0)
- 8GB RAM minimum
- Operating System: Windows 11, macOS 12+, or Ubuntu 20.04+

## Installation

### Backend Setup
```bash
cd backend
npm install
# Configure MongoDB connection in config/database.js
# Set up OAuth credentials in config/oauth.js
npm start
```

### Attack Simulator Setup
```bash
cd attack-simulator
pip install -r requirements.txt
python credential_stuffer.py
```

## Reproduction Instructions
1. Start MongoDB: `mongod`
2. Start backend server: `cd backend && npm start`
3. Run attack simulation: `cd attack-simulator && python credential_stuffer.py`
4. Results saved to `data/attack_results.csv` and `data/attack_metrics.json`

## Data Files
- `attack_results.csv`: Per-request logs (202 requests)
- `attack_metrics.json`: Aggregated statistics
- `combolist.csv`: 101 test credentials (100 synthetic + 1 valid)

## Ethical Considerations
All experiments conducted on localhost with synthetic data. No real user credentials used. See `supplementary/ethical-approval.md` for details.

## License
This project is licensed under the MIT License - see LICENSE file for details.

## Contact
For questions: researchwithharsh@gmail.com
