on run argv
  set inPath to item 1 of argv
  set outPath to item 2 of argv
  tell application "Microsoft PowerPoint"
    open (POSIX file inPath)
    delay 3
    set p to active presentation
    save p in (POSIX file outPath) as save as PDF
    close p saving no
  end tell
end run
