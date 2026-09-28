-- Harmless reproduction of the AMOS bmodule password dialog, for screenshotting only.
-- It ONLY draws the window. It does not read, validate, store, or send anything.
-- Whatever you type is discarded when the window closes. No dscl, no network, no files.
-- Source of the exact wording/appearance: stage3.deob.txt in this folder.

display dialog "To run the application you need to change the settings for its operation." & return & "Please enter password for continue:" default answer "" with icon caution buttons {"Continue"} default button "Continue" with title "System Preferences" with hidden answer

-- The line above returns a record with the typed text; we deliberately never bind it,
-- so nothing is captured. The script ends here.
