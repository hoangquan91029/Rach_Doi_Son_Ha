# Additive amendment to the independent motion review

This amendment withdraws the warning in the original review that the original travel APNG/GIF compounded ground scrolling with sprite movement. That warning was incorrect. The original review remains unchanged and preserved; this note records the correction separately.

In the frozen `pilot.py` (`b5c1472cce875cec649e8331b4f91da2bef64a7f57b910109a360ad727fb62e4`), line 224 builds each travel frame with `grid(480,256)` at its default zero offset, then places the sprite at an advancing `root_x`. The ground stays static as the character root moves, so these APNG/GIF previews do not compound background and sprite velocity. They are valid diagnostics for the eight held cels.

The review itself used the separate fixed-root/scrolling-ground browser preview with the engine sprite timing sampler, not the travel APNG/GIF. This correction therefore does not change the independent verdict: tracked held-cel toe slip remains 3.9088 px against the 2 px gate, and the D07 eight-frame walk remains `INDEPENDENT_MOTION_FAIL_NARROW`.

I did not stop or signal the root preview server on port 8766. My only server interactions were a read-only local HTTP GET check and opening the page in the browser; no cleanup command or process signal was issued.
