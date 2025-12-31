# LittleWorld

A 2D simulated world where AI characters live, act, and interact with each other and the player.

## Overview

LittleWorld is a real-time simulation where AI-powered characters with distinct personalities exist in a shared 2D space. Each character can move, communicate, and interact with objects in the environment. The player also participates as a character in this world.

## Features

- **2D Visual World**: Built with pygame, featuring a green ground where characters move and interact
- **AI Characters**: Each character is powered by an LLM (GPT-4o initially) with unique personalities
- **Real-time Gameplay**: Characters act continuously in real-time
- **Vision System**: Characters have a vision radius and can only perceive things within their range
- **Communication**: Characters can talk to each other and to the player
- **Player Participation**: The player appears as a character on screen and can move and communicate

## Technical Architecture

### Phase 1 (Current)
- **LLM**: GPT-4o API for character decision-making and dialogue generation
- **Personality System**: Character personalities defined in `.md` files
- **Configuration**: Decision intervals, vision radius, and other parameters are configurable (default: 3 seconds between decisions)
- **API Key**: Stored in `.env` file

### Phase 2 (Future)
- Replace API LLM with local models
- Fine-tune models for specific character personalities
- Database integration to store character actions and history

