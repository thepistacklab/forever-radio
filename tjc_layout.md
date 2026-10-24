# Forever Radio – making the TJC screen file (one time only)

Display: TJC4832T135_011 (3.5", 480×320). The Pi draws all the text and the volume bar
(`tjc_class.py`), so the screen file only needs **three fonts** and an **empty page**.
Viewers don't do any of this. They download the finished `ForeverRadio.tft` and copy it to a microSD card.

## 1. New project (USART HMI)

- **新建 (New)**, then model **TJC4832T135_011**, **横屏 (landscape)**, encoding **utf-8**.
- Leave the page empty. Optional: set the page **bco** to **0** (black).

## 2. Three fonts: 工具 (Tools) → 字库制作 (Font Generator)

| Make in this order | 字高 (Height) | 字库名称 (Name) |
|---|---|---|
| font 0 | 24 | small |
| font 1 | 32 | medium |
| font 2 | 40 | big |

The same for all three:

- **编码 (Encoding):** utf-8
- **字体 (Font):** Arial
- **字体抗锯齿 (Smoothing):** ticked
- **范围 (Range):** **ASCII字符**, **not** 所有字符 (all characters). The driver turns accented letters into plain ones.

Click **生成字库 (Generate)**, and answer **Yes** to add it to the project.

## 3. Compile and load

1. Click **编译 (Compile)**. It must show 0 errors.
2. **文件 (File) → 打开编译文件夹 (Open build folder).** Copy the `.tft` file, and rename it `ForeverRadio.tft`.
3. On a FAT32 microSD card, put only `ForeverRadio.tft` in the root.
4. Power off. Insert the card into the TJC and power on. It installs itself.
5. When it's finished, power off, remove the card, and power on again. The screen should be blank.

## 4. Test from the Pi

```bash
sudo apt install -y python3-serial
python3 ~/tjc_class.py
```
