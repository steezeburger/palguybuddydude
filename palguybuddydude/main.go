package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
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

	body, err := io.ReadAll(resp.Body)
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

	ticker := time.NewTicker(15 * time.Second)
	defer ticker.Stop()

	previousPlayers := make(map[string]struct{})
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

			currentPlayers := make(map[string]struct{})
			for _, player := range info.Players {
				currentPlayers[player.Name] = struct{}{}
				if !initialFetch {
					if _, exists := previousPlayers[player.Name]; !exists {
						message := fmt.Sprintf("Player joined: %s", player.Name)
						if err := notifyDiscord(webhookURL, message); err != nil {
							log.Printf("Failed to send Discord notification: %v", err)
						}
					}
				}
			}

			if !initialFetch {
				for player := range previousPlayers {
					if _, exists := currentPlayers[player]; !exists {
						message := fmt.Sprintf("Player left: %s", player)
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
