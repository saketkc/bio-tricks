# Installing Linuxbrew on Cluster

## Step 1

Edit `setup.sh` to edit `HOME` variable.
This is the ONLY variable that you should edit.

`HOME` is the location where whole of the `linuxbrew` setup
would sit, including cache.

There is limited space available in `~/` and hence  
the script symlinks `~/.cache` to `linuxbrew_cache` inside
`HOME` folder. This is required because `linuxbrew`
relies on `~/.cache` for downloading.

## Step 2

`bash step1.sh`


## Step 3

`bash step2.sh`

