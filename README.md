# Contact Book App

So I built this contact manager thing because honestly I was tired of scrolling through my phone contacts all the time. Thought it'd be easier to have a desktop version where I could actually search and organize stuff properly.

## What's this about?

It's basically a digital address book. You can add people's info (name, phone, email, address), edit them later if something changes, delete contacts you don't need anymore, and search through everything. Pretty straightforward tbh.

## Getting it to work

You'll need Python installed - I'm using 3.8 but anything recent should be fine. The good news is it only uses tkinter which comes built-in with Python, so no pip installs or anything annoying like that.

Just run:
```bash
python contact_book.py
```

And boom, window pops up and you're good to go.

## How to use it

Left side is where you add/edit contacts. Right side shows all your contacts in cards. 

**Adding someone:**
- Type their name and phone (these are required)
- Email and address are optional, leave blank if you want
- Hit "Add Contact" button
- Done

**Editing:**
- Click the green "Edit" button on any contact card
- Make your changes in the form
- Click "Save Changes"
- Or hit "Cancel Edit" if you change your mind

**Deleting:**
- Red "Delete" button on each card
- It'll ask you to confirm so you don't accidentally nuke someone

**Searching:**
- Just start typing in the search box at the top
- Searches through names and phone numbers as you type
- Real-time filtering, no need to hit enter or anything

## The data storage thing

All your contacts get saved to a `contacts.json` file in the same folder as the script. It's just a JSON file so you can open it in any text editor if you want to see what's in there or backup your data.

The file gets created automatically the first time you add a contact. If you delete it, you'll lose all your contacts (obviously), but the app won't crash - it'll just start fresh.

## Some design choices I made

- Went with a two-panel layout because it felt more intuitive than having everything crammed together
- Used emoji icons (📞 📧 📍) instead of text labels because why not, they look better imo
- Cards show different info depending on what you filled in - like if there's no email, it just doesn't show that row
- Alphabetical sorting happens automatically, seemed like the logical default
- The search placeholder text disappears when you click in it, comes back if you don't type anything

## Stuff that could be better

There's definitely room for improvement if I ever feel like working on this again:
- No phone number validation right now, you could type letters and it wouldn't complain
- Email validation would be nice too
- Maybe add categories or tags for organizing contacts
- Could add import/export for CSV files
- A backup feature would be smart
- Dark mode? Everyone loves dark mode

But for now it does what I need it to do so I'm not rushing to add features.

## Known issues

Nothing major that I've found. The scrolling works fine, search is pretty responsive. One thing I noticed is if you have a TON of contacts (like hundreds) it might get a bit sluggish but I haven't tested with that many yet.

Oh and the window size is fixed at 950x650 which works on my screen but might be weird on really small displays. Could make it resizable but haven't bothered yet.

## Why I coded it this way

Used tkinter because it's simple and cross-platform. No need to mess with web frameworks or anything heavy. The class-based approach keeps things organized even though it's not a huge codebase.

JSON for storage because it's human-readable and easy to work with. Could've used SQLite or something but that felt like overkill for what's essentially a personal tool.

## License and stuff

Do whatever you want with this code. Copy it, modify it, learn from it, I really don't care. No attribution needed. If you make something cool with it though I'd be curious to see what you did.

---

That's about it! Feel free to fork this and make it better. Or don't, that's cool too. Just thought I'd share in case anyone else finds it useful.
