from lists import *
from B2_ConverterHelpers import getFiles

errorFiles = []


def toSecs(col):
    if ":" in col:
        lis = col.split(":")
        hr = lis[0]
        col = lis[1]

    if "'" in col:
        lis = col.split("'")
        min = lis[0]
        sec = lis[1]

    nueMin = hr * 60
    min = min + nueMin
    nueSec = min * 60
    sec = sec + nueSec

    return sec


print(csvSesDir)

# combine years and leagues into separate files
for yr in yrs[0]:
    for lge in lges[0]:
        files = getFiles(csvSesDir, f"{yr}-{lge}*.csv")
        if len(files) > 0:
            frames = []
            lenGoal = 0

            for file in files[0]:
                df = pd.read_csv(file)
                df.drop(["sec_fiv", "sec_six", "sec_sev", "sec_eig"])

                df["lap_sec"] = toSecs(df["lap_time"])
                df["one_seconds"] = toSecs(df["sec_one"])
                df["two_seconds"] = toSecs(df["sec_two"])
                df["thr_seconds"] = toSecs(df["sec_thr"])
                df["four_seconds"] = toSecs(df["sec_four"])

                df["lap_scaled"] = df["lap_sec"] / df["lap_sec"].abs().max()
                df["one_scaled"] = df["one_seconds"] / df["one_seconds"].abs().max()
                df["two_scaled"] = df["two_seconds"] / df["two_seconds"].abs().max()
                df["thr_scaled"] = df["thr_seconds"] / df["thr_seconds"].abs().max()
                df["four_scaled"] = df["four_seconds"] / df["four_seconds"].abs().max()

                frames.append(df)
                lenGoal = lenGoal + len(df)

            wholeFrame = pd.concat(frames)


            nueFile = f"{yr}-{lge}-Season-try"
            wholeFrame.to_csv(f"{csvSeasonDir}{nueFile}.csv", index=False)
            lenActual = len(wholeFrame)
            print(f"{nueFile}")
            if lenActual != lenGoal:
                print(f"\nerror \n{nueFile}\ngoal length:  {lenGoal}\nactual length:  {lenActual}\nend error\n")
                errorFiles.append(nueFile)

if len(errorFiles) != 0:
    print("\n\nError Files:")
    for i in errorFiles:
        print(i)

print("\nFinished\n\n")
