# paulstretch
Audio processing algorithm to stretch audio files by huge amounts without artefacts.

The algorithm being used here is "paulstretch", by [Paul Nasca](http://www.paulnasca.com/). You split an audio signal up into multiple overlapping windows, fourier transform each window, randomize the phase, and then inverse fourier transform and reconstitute using an amplitude mask.

Randomizing the complex phases is the key step here, as this hides any audio tearing/compression artefacts that would otherwise be painfully obvious when sounds are slowed down too much.

Extremely in-progress, will update this README later.

Progress:
 - [x] File I/O
 - [x] Implement window splitting
 - [x] Implement window reconstitution
 - [x] Implement basic amplitude mask
 - [ ] Implement dynamic amplitude mask
 - [ ] Implement FFT and IFFT
 - [ ] Implement actual stretch effect
  
