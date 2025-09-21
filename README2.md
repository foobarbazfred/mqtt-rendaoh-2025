# 🕹️ MQTT Renda-Oh 2025: The Real-Time Button-Mash King Game

<img src="assets/images/rendaoh_kanji.png" width="500">

MQTT Renda-Oh 2025 is a competitive button-mash game designed to leverage the MQTT protocol for real-time, distributed play [1, 2]. This project serves as an advanced educational showcase of IoT and embedded systems, created for the GitHub "For the Love of Code" hackathon (July 16 – September 22, 2025) [3, 4].
## 🌟 Project Overview: The Joy of Extreme Real-Time Messaging
The primary concept of Renda-Oh (King of Mashing) is to have players compete by pressing physical buttons as many times as possible within a set period [1, 5].
The Hackathon Hook: Absurd Real-Time Tactility (Joyfulness & Ingenuity)
The original prototype prioritized implementation simplicity by reporting scores in periodic batches [6, 7]. This enhanced version flips that design:
-  1 Click = 1 MQTT Message: Every single button press immediately triggers an MQTT report message publication [Conversation History]. This maximizes the feeling of tactility and the "absurdity" of flooding the network with rapid, real-time updates for maximum vibe [Conversation History].
-  The Race for Speed: The winner is the player who achieves the highest click count when the competition ends [5].

## 🏆 Hackathon Category
This project is submitted under:
Category 1: Buttons, Beeps, and Blinkenlights [8, 9].
-  Fit: This category seeks hardware hacks that blink, beep, buzz, or surprise [8]. Renda-Oh is fundamentally an interactive, physical, and tactile system utilizing buttons, Piezo speakers, and color LEDs to manage the competitive experience [10].

## ⚙️ Key Technical Enhancements (Execution & Difficulty)
The high-frequency messaging goal required solving critical constraints found in the original prototype [11]:
- PIO for Optimized Input (Technical Difficulty): To ensure accurate counting and prevent CPU core resource consumption due to software debouncing [12], the PIO (Programmable Input/Output) feature of the Raspberry Pi Pico 2 W is utilized to count button presses independently of the main microcontroller process [1, 13-15].
- High-Performance MQTT Broker Requirement (Execution): The high volume of "1 click = 1 message" reports necessitates a robust broker. The original public broker failed due to quota limitations (0x97: Quota Exceeded) [11]. Therefore, this version requires a high-performance broker like AWS IoT Core to handle the high message rate and maintain low latency [44, 65, Conversation History].
- Robust State Synchronization: Critical game state transition messages (change-state) use MQTT QoS: 1 to guarantee delivery [16]. The system implements a retransmission mechanism specifically to handle 0x97: Quota Exceeded responses from the broker, ensuring crucial messages are not lost and the game proceeds synchronously [11, 12].

## 🖼️ Project Visuals (Appearance and Gameplay)
The system consists of the GameController and multiple GamePlayers [5, 10].
- GamePlayer Setup: GamePlayers are built using MicroPython-enabled boards (e.g., Raspberry Pi Pico 2 W/Pico W) connected to a physical switch, a Color LED (NeoPixel), and a Piezo Speaker [10, 14, 17].
- Game Flow Feedback:
    - Countdown: Game start and stop are signaled by synchronized flashing LED patterns and Piezo speaker melodies [10].
    - Live Score Indicator: During the match, the Color LED functions as an indicator, visualizing the click count of the player and the opponent. The length of the indicator represents the lead, showing which player is currently ahead [10, 18].
    - Victory: After aggregation, synchronized sound and victory displays indicate the winner [5].
- Distributed Play: Though the demo units may be adjacent, all score updates and state changes are routed via the MQTT broker, enabling competition between players in remote locations [18, 19].
(Note: Actual README would embed Photo 1, Photo 2, and Figure 3 (GamePlayer Circuit Diagram) here.)

## 🧩 Software Architecture
The software structure centralizes complex networking and state logic into a common class [14].
1. Core Modules
The software is structured around three key classes [14]:
- Controller Class: Handles game progression instructions, score aggregation, and victory determination [14].
- Player Class: Manages user output via the Color LED and Piezo speaker, and displays the opponent's score periodically [14].
- GameAgent Class: The core management layer, consolidating MQTT message sending/receiving and the game state machine logic [14].
(Note: Actual README would embed Figure 4 (Software Structure Diagram) here.)
2. Game State and Synchronization
- State Machine Implementation: The game flow is divided into 12 distinct states (e.g., countdowns, reporting, result display) [17].
- Synchronous Transitions: All GamePlayers transition states simultaneously, triggered by synchronous instructions (change-state messages) issued by the GameController [6, 17]. This state transition logic is implemented declaratively using a common state transition table (dictionary format) within the shared GameAgent class [20, 21].
3. Communication Protocol (MQTT Topics)
  
Three main MQTT message types govern the game flow [16]:
1. change-state: Instructs state progression (set to QoS: 1) [16].
2. report: GamePlayer reports the user's latest click count (high frequency in this version) [52, Conversation History].
3. summary: GameController shares aggregated click counts for all participants (used for reference display during the match) [16, 22].

## 📚 Educational Highlights
This project provides practical, hands-on experience in [23, 24]:
- Implementing robust communication and state synchronization using the MQTT protocol [24].
- Advanced embedded techniques like using PIO for reliable, low-latency input counting [15, 23].
- Embedded development using MicroPython on modern microcontrollers [13].
- Integrating physical I/O: switches, SPI-connected LCDs, LEDs, and sound effects [24].

## 💻 Setup and Dependencies

Hardware Requirements:
- GamePlayer (MicroPython): Raspberry Pi Pico 2 W (RP2350) or Pico W [1, 13, 17].
- GameController (Python/MicroPython): AtomS3 (ESP32-S3) or Raspberry Pi 4 [13, 17].
- I/O Components: Pushbutton switch, Color LED (NeoPixel Ring), Piezo Speaker [10, 14].
Software & Service Requirements:
- Embedded OS: MicroPython [13].
- Python: Python 3 (for Controller if not using MicroPython) [1].
- MQTT Client: umqtt.simple (MQTT V3) for GamePlayer, paho-mqtt (MQTT v5) for Controller (if using Python 3) [1, 25].
- MQTT Broker: AWS IoT Core or equivalent high-performance, low-latency broker with permissive quota policies is required for the "1 click = 1 message" mode [12, 13].

⚠️ Note on Dependencies: For stable operation in the high-frequency mode, relying on a public broker with strict quotas is discouraged. Please note any paid services used (e.g., AWS IoT Core) in your submission [13, 26].

--------------------------------------------------------------------------------
For detailed setup instructions, circuit diagrams, and PIO source code, please refer to the src directory or the project Wiki.
We encourage feedback, collaboration, and chaos! Questions and suggestions are welcome via Issues or Pull Requests! [27]
