# GH-Grabber
I wanted a tool that could easily find the items from a specific user, or if i knew the name of their repository(s) I wanted. This will find the user/repo and get the releases for machine I am on or clone them.

```python
    GitHub Repo Downloader and Installer Script

    Usage:
        GH-Grabber.py -s <software_name>
        GH-Grabber.py -a <author_name>

    Arguments:
        -s, --software    Specify the software name to search for repositories.
        -a, --author      Specify the author name to find repositories by author.

    Examples:
        GH-Grabber.py -s example-software
        GH-Grabber.py -a dewalt-arch
```
- Checking for Author
```
blindpentester@wpad:~$ python3 GH-Grabber.py -a dewalt-arch

Select a repository by number:
[ 1 ] Dewalt-arch/bettermap (⭐ 21)
[ 2 ] Dewalt-arch/kioptrix-vmware (⭐ 6)
[ 3 ] Dewalt-arch/pimpmy-phprevshell (⭐ 8)
[ 4 ] Dewalt-arch/pimpmyadlab (⭐ 125)
[ 5 ] Dewalt-arch/pimpmyi3 (⭐ 12)
[ 6 ] Dewalt-arch/pimpmyi3-config (⭐ 4)
[ 7 ] Dewalt-arch/pimpmykali (⭐ 1868)

Enter the number of the repository you want to select: 7
[  ୧༼ಠ益ಠ༽୨  ] Failed to fetch releases for pimpmykali. HTTP Status Code: 404
[ ಠ‿ಠ ] Cloning pimpmykali...
Cloning into 'pimpmykali'...
remote: Enumerating objects: 2791, done.
remote: Counting objects: 100% (879/879), done.
remote: Compressing objects: 100% (334/334), done.
remote: Total 2791 (delta 564), reused 762 (delta 545), pack-reused 1912 (from 1)
Receiving objects: 100% (2791/2791), 506.78 KiB | 1.57 MiB/s, done.
Resolving deltas: 100% (1190/1190), done.
blindpentester@wpad:~$ 
```
- Checking for software
```
blindpentester@wpad:~$ python3 GH-Grabber.py -s httpx

Select a repository by number:
[ 1 ] encode/httpx (⭐ 12998)
[ 2 ] projectdiscovery/httpx (⭐ 7461)
[ 3 ] ossrs/httpx-static (⭐ 641)
[ 4 ] Colin-b/pytest_httpx (⭐ 344)
[ 5 ] frankie567/httpx-oauth (⭐ 140)
[ 6 ] janko/down (⭐ 1025)
[ 7 ] Colin-b/httpx_auth (⭐ 114)
[ 8 ] AndreLouisCaron/httpxx (⭐ 56)
[ 9 ] HoneyryderChuck/httpx (⭐ 187)
[ 10 ] pandao/httpx.js (⭐ 53)
[ 11 ] t3l3machus/Synergy-httpx (⭐ 122)
[ 12 ] servicex-sh/httpx (⭐ 130)
[ 13 ] lundberg/respx (⭐ 597)
[ 14 ] unjs/httpxy (⭐ 188)
[ 15 ] frankie567/httpx-ws (⭐ 101)
[ 16 ] JacksonTian/httpx (⭐ 46)
[ 17 ] bojanz/httpx (⭐ 92)
[ 18 ] ringabout/httpx (⭐ 90)
[ 19 ] florimondmanca/httpx-sse (⭐ 113)
[ 20 ] whoisavicii/Masscan2Httpx2Nuclei-Xray (⭐ 75)
[ 21 ] johtso/httpx-caching (⭐ 64)
[ 22 ] karpetrosyan/hishel (⭐ 157)
[ 23 ] romis2012/httpx-socks (⭐ 77)
[ 24 ] obendidi/httpx-cache (⭐ 50)
[ 25 ] nickrusso42518/slt-py-httpx (⭐ 18)
[ 26 ] coffeehc/httpx (⭐ 15)
[ 27 ] grafana/k6-jslib-httpx (⭐ 13)
[ 28 ] z0mb13s3c/httpx2bbrf (⭐ 12)
[ 29 ] ramnes/notion-sdk-py (⭐ 1744)
[ 30 ] chassing/uplink-httpx (⭐ 15)

Enter the number of the repository you want to select: 2
Detected system: linux, architecture: x86_64
Available asset: httpx_1.6.8_checksums.txt
Available asset: httpx_1.6.8_linux_386.zip
Available asset: httpx_1.6.8_linux_amd64.zip
Available asset: httpx_1.6.8_linux_arm.zip
Available asset: httpx_1.6.8_linux_arm64.zip
Available asset: httpx_1.6.8_macOS_amd64.zip
Available asset: httpx_1.6.8_macOS_arm64.zip
Available asset: httpx_1.6.8_windows_386.zip
Available asset: httpx_1.6.8_windows_amd64.zip
Downloading httpx_1.6.8_linux_amd64.zip...
Downloaded httpx_1.6.8_linux_amd64.zip successfully.
Unzipping httpx_1.6.8_linux_amd64.zip...
Extracted files to 'httpx_1.6.8_linux_amd64.zip_extracted' directory.
[ ಠ‿ಠ ] Testing httpx...
[ ಠ‿ಠ ] Detected executable: httpx
[ ಠ‿ಠ ] httpx installed and tested successfully.

```

- If repo already exists...
```
blindpentester@wpad:~$ python3 GH-Grabber.py -s FlexScanner

Select a repository by number:
[ 1 ] blindpentester/FlexScanner (⭐ 2)
[ 2 ] EivindRoslyng/flexscanner (⭐ 0)
[ 3 ] Ignacio-Ferrante/FlexScanner (⭐ 0)
[ 4 ] rahul-mitra13/flexScanner (⭐ 0)
[ 5 ] khmikkelsen/FlexScanner (⭐ 0)

Enter the number of the repository you want to select: 1
Detected system: linux, architecture: x86_64
Available asset: FlexScanner
[ ୧༼ಠ益ಠ༽୨ ] No suitable release found for linux on x86_64. Cloning repository instead...
[ ಠ‿ಠ ] Directory 'FlexScanner' already exists. Pulling latest changes...
Already up to date.
```
