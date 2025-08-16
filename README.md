# MQTT Renda-Oh 2025: Real-Time Button Mash Battle with IoT

This project was created for GitHub's "For the Love of Code 2025" hackathon.  
It is a revamped version of the original MQTT-based button mash game, designed to be more fun, educational, and technically refined.

Using MicroPython and the AtomS3 microcontroller, players compete in real-time by pressing buttons as fast as possible.  
Each device sends its score via MQTT, and the results are displayed on a GC9107 LCD screen using SPI communication.  
The project is designed to help beginners learn about hardware/software integration, SPI protocols, and MQTT messaging in a playful way.

## Tech Stack
- AtomS3 (ESP32-S3)
- MicroPython
- GC9107 LCD (SPI)
- MQTT (Pub/Sub model)
- PIO (for SPI optimization)

## Target Audience
- Beginners to intermediate learners in IoT and embedded systems
- Educators and workshop facilitators
- Anyone who loves mashing buttons and learning how it works under the hood

## Hackathon Category
Category 1: Buttons, beeps, and blinkenlights
