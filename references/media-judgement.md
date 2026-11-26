# How an agent judges copyright and identifies media

Observed 2026-11-25 in Claude Code (remote session, Windows host), in a session about a piano arrangement of a commercial song. What the agent does and does not do when a request touches copyrighted audio or images, written down so a user can predict its behaviour instead of guessing at a hidden system.

## There is no detector

- No background scan, database or external service checks a request for copyright.
- A judgement comes from training knowledge applied to what the user said. A named song ("Karma Police", 1997) is known to be under copyright the same way a novel's publication date is known.
- Tools join in only when the agent chooses to run them, and it should say so.
- The agent can describe its behaviour but cannot inspect its internals to prove why it reached a judgement. Treat its explanations as reports, not proofs.

## Audio

- In this harness the model has no audio input. It cannot hear a file and recognise it.
- What a file is can only be learned through the tools anyone would use: tags (`ffprobe`: title, artist, album, sometimes a copyright field), the filename, or a fingerprint lookup (Chromaprint/AcoustID, then MusicBrainz). None of these run by default.
- A file with no tags, no context and no fingerprint lookup is unknown to the agent.

## Images of real people

- The model sees images but does not identify real people from facial features. An unlabelled photo is described (beard, guitar, stage, era of the colours), not named. This is a deliberate limit, not missing knowledge.
- Context changes it: a filename, a caption, or the user saying who it is.
- EXIF and IPTC fields (photographer, copyright, caption) are read only if the agent runs a tool for it.
- Who is in a photo says nothing about who owns its copyright. The photographer or agency holds the copyright; the subject or estate holds separate rights of publicity over commercial use of name and likeness. Provenance and credit lines settle ownership, not the face.

## The rules it applies

- Default: copyrighted unless something shows otherwise.
- A recording carries two copyrights: the composition (songwriter, publisher) and the sound recording (usually the label). Both must be clear.
- US public domain as of 2026: compositions published 1930 or earlier. Sound recordings follow the Music Modernization Act: before 1923 free; 1923-1946 free 100 years after release; 1947-1956 after 110 years; 1957 to 15 Feb 1972 protected until 2067. Other countries count differently.
- Clear sources: audio the user or a local model generated, the user's own recordings, CC0 or public-domain archives (Musopen, parts of the Internet Archive), Creative Commons under its terms, royalty-free libraries within their licence. Streaming, YouTube or CD rips are copyrighted by default.
- When the evidence says copyrighted, the agent declines to transcribe, recreate or re-arrange it (a piano arrangement reproduces the composition), even for personal use, and offers routes such as licensed sheet music, stem separation run by the user on a copy they own, or an original piece in the same mood. Fair use is a legal call the agent does not make for the user.
- Splitting the work across many chained sessions does not change the judgement.
