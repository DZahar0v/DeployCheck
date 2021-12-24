# DeployCheck
Python script for check that deployed contracts equal to contract in github repo

# Dependencies
[Meld](https://meldmerge.org/)

# Usage
- Specify directory for downloading files from etherscan in Config -> directory
- For each file for comparison specify it's name, etherscan address, local path for file which was cloned from git (e.g. ["ACL", "0x523da3a8961e4dd4f6206dbf7e6c749f51796bb3", "./gearbox/contracts/core/ACL.sol"])
- Run `python LoadContracts.py` 
