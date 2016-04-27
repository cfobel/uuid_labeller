# Example #

This example demonstrates:

 - Global UUID label replacement.
 - Unique UUID label replacement.
 - Date replacement.
 - Date and time replacement.

# Instructions #

 1. Open `input.svg` in Inkscape.
 2. Select `Extensions > UUID > UUID labeller...` from menu.
 3. In the `UUID labeller` dialog:
     - In the first text box enter:

            batch1[:6],<batch1>[:8],batch2[:6],<batch2>[:8],datetime,date

     - Check the `Save tags to file` checkbox.
 4. Click `Apply`.
 5. Click `OK`.

After completing the steps above:

 - The displayed output should be similar to `output.svg` (but with different
   UUIDs, date, time, etc.).
 - The contents of output comma-separated values file should be similar to 
   `output.csv` (but with different UUIDs, date, time, etc.).
