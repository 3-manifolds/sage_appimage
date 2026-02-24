# sage_appimage

This repoository provides AppImages for running SageMath on linux,
including linux running in Windows WSL2.  The releases are built on a
manylinux2014 docker image, so the AppImage should run on linux
systems which use glibc version 2.17 or later.

**Linux Installation**
1. Download an AppImage for SageMath `X.Y` from the Releases page.
2. Create `~/bin` (if necessary): `mkdir -p ~/bin`
3. Move the AppImage for Sage X.Y into `~/bin`: `mv ~/Downloads/SageMath-X.Y-x86_64.AppImage ~/bin`
4. Make it executable: `chmod +x ~/bin/SageMath-X.Y-x86_64.AppImage`
5. Create a convenient symlink: `ln -s SageMath-X.Y-x86_64.AppImage ~/bin/sage`

You will need to have `~/bin` in your `PATH` to run sage conveniently.
This should happen automatically, but you may need to log out and log
back in if your `~/bin` directory did not already exist in step 2.

If you are using a linux desktop system, such as Gnome or KDE, you can
add Sage to the desktop application menu and create an icon which can
be pinned to the Ubuntu Dash or KDE Taskbar by running the command:
`sage --install-desktop`
(That command creates
`~/.local/share/applications/sagemath.desktop`
and
`~/.local/share/icons/sage_icon.svg`.)

**Windows WSL2 Installation**

The commands listed above should be run in your WSL powershell,
except that you should replace step 3 by:

3'.  Move the AppImage into
`~/bin`: `mv /mnt/c/Users/<your id>/Downloads/SageMath-X.Y-x86_64.AppImage
~/bin` (Replace `<your id>` with your Windows user id and `X.Y` by the Sage version.)

**Usage**

To run sage, open a linux terminal or WSL powershell and type`sage` or
`sage -n` or `sage -n jupyterlab`.

Alternatively, on a linux desktop, after pinning the application icon,
just click on the icon.  This will start the command line version of
Sage.  You can arrange to launch a notebook by editing the
sagemath.desktop file to add `-n` on the `Exec` line.

The AppImages include the python tkinter module, which works in Sage
(after running %gui tk) on a linux desktop.  It does not work in WSL
since it requires an X server.
