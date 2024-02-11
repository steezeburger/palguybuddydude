package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

type Player struct {
	Name      string `json:"name"`
	PlayerUID string `json:"playeruid"`
	SteamID   string `json:"steamid"`
}

type ServerInfo struct {
	Players       []Player `json:"players"`
	ServerName    string   `json:"serverName"`
	ServerVersion string   `json:"serverVersion"`
}

// fetchServerInfo makes an HTTP GET request to the server info API
func fetchServerInfo(apiURL string) (ServerInfo, error) {
	resp, err := http.Get(apiURL)
	if err != nil {
		return ServerInfo{}, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return ServerInfo{}, err
	}

	var info ServerInfo
	err = json.Unmarshal(body, &info)
	if err != nil {
		return ServerInfo{}, err
	}

	return info, nil
}

// notifyDiscord sends a message to a Discord webhook
func notifyDiscord(webhookURL string, message string) error {
	payload := map[string]string{"content": message}
	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		return err
	}
	_, err = http.Post(webhookURL, "application/json", bytes.NewBuffer(jsonPayload))
	return err
}

func main() {
	baseURL := os.Getenv("RCON_BUDDY_HOST")
	apiURL := fmt.Sprintf("http://%s/info", baseURL)
	webhookURL := os.Getenv("DISCORD_WEBHOOK_URL")

	log.Printf("Starting palguybuddydude!")

	ticker := time.NewTicker(15 * time.Second)
	defer ticker.Stop()

	previousPlayers := make(map[string]Player)
	initialFetch := true

	for {
		select {
		case <-ticker.C:
			info, err := fetchServerInfo(apiURL)
			if err != nil {
				log.Printf("Failed to fetch server info: %v", err)
				continue
			}

			if initialFetch {
				log.Printf("Initial server info fetched: %+v", info)
			}

			log.Printf("Current players: %+v", info.Players)

			currentPlayers := make(map[string]Player)
			for _, player := range info.Players {
				// NOTE - i think this fixes the issue where there's a duplicate user
				if player.PlayerUID == "00000000" {
					log.Printf("Skipping fake duplicate player: %+v", player)
					continue
				}
				currentPlayers[player.PlayerUID] = player
				if !initialFetch {
					if _, exists := previousPlayers[player.PlayerUID]; !exists {
						message := fmt.Sprintf("Player joined: %s", player.Name)
						if err := notifyDiscord(webhookURL, message); err != nil {
							log.Printf("Failed to send Discord notification: %v", err)
						}
					}
				}
			}

			if !initialFetch {
				for uid, player := range previousPlayers {
					if player.PlayerUID == "00000000" {
						log.Printf("Skipping fake duplicate user: %+v", player)
						continue
					}
					if _, exists := currentPlayers[uid]; !exists {
						message := fmt.Sprintf("Player left: %s", player.Name)
						if err := notifyDiscord(webhookURL, message); err != nil {
							log.Printf("Failed to send Discord notification: %v", err)
						}
					}
				}
			}

			previousPlayers = currentPlayers
			if initialFetch {
				initialFetch = false
			}
		}
	}
}
