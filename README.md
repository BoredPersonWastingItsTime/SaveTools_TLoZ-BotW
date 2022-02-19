# SaveTools_TLoZ-BotW

A little tool I created to modify a bunch of things in Breath of the Wild's game_data.sav

---
My aim when I started was to fix PorchItem ordering bug in [MarcRobledo's BotW save editor](https://www.marcrobledo.com/savegame-editors/zelda-botw/) wich cause newly added items not to have properties (weapons with no modifiers, clothes blue by default, etc.). However, I ended up making more functions and I though it would be nice to share it. Also, sorry in advance for the bad programming, I just learned Python. Disclaimer: use at your own risk.

There are references and credits inside the spreadsheets and scripts. If I missed any, please tell me (when I started I didn't think I would share this). Other useful resources to look at when editing game_data.sav:
- [List of shrines](https://github.com/leoetlino/botw-shrine-rush/blob/master/shrine_rush_order.csv) and [more](https://github.com/leoetlino?tab=repositories&q=botw) by leoetlino
- [Datamined stuff](https://github.com/MrCheeze/botw-tools) and [more](https://github.com/MrCheeze?tab=repositories&q=botw) by MrCheeze
- I should add more when I remember or find them.

---
I wrote this for Python 3.8.10 and BotW 1.6.0-switch, to use it:
1. install [Python](https://www.python.org/downloads/#:~:text=python%203.8.10) if you havent already
2. clone or [download](https://github.com/BoredPersonWastingItsTime/SaveTools_TLoZ-BotW/archive/refs/heads/main.zip) the source
3. extract to an empty folder
4. place game_data.sav into the same folder
5. double click BotW_Edit_v#.py
6. follow instructions

Tip: while in "fmenu", you can type only the first letters of the submenu instead of the whole word (like "e", "ed" or "edi" instead of "edit").

PD: If you find this useful and want to modify & share this, suggest me which license I should add (it's very confusing to me, and I'm happy with any that includes 'give credits' stuff).
