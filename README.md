# agoranov-hackathon

Projet Hackathon LeRebours: Transcription Audio en Temps Réel

Ce projet a été développé lors du hackathon "Startups à l'École" en collaboration avec la startup [Logbook](https://logbook.co/). L'objectif était d'implémenter une fonctionnalité de **transcription audio en temps réel** pour améliorer l'application Logbook, qui aide les enseignants à fournir des retours audio personnalisés aux élèves.

Nous avons créé une Preuve de Concept (POC) d'une application web qui permet aux utilisateurs d'enregistrer de l'audio et de voir la transcription apparaître en direct, quasi instantanément.

      
![Page de connexion de l'application](https://raw.githubusercontent.com/drewano/agoranov-hackathon/main/connexion.png)


## Fonctionnalités Clés

*   **Authentification utilisateur** (Inscription/Connexion via Supabase Auth).
*   **Enregistrement audio** depuis le navigateur.
*   **Transcription en temps réel** via WebSocket (utilisant l'API Gladia).
*   Affichage de la transcription au fur et à mesure, avec horodatage des segments.
*   **Stockage** des enregistrements audio et des transcriptions associées (Supabase Storage & Database).
*   Consultation et gestion des enregistrements passés (lecture audio, affichage transcription, suppression).
*   **Copie** de la transcription générée.

## Technologies Utilisées

*   **Frontend:** React, TypeScript, Vite, Tailwind CSS
*   **Backend:** Python, Flask, WebSocket
*   **Services:** Supabase (Auth, Database, Storage), Gladia API (pour la transcription)

## Vidéo de Présentation & Interview

Pour une présentation plus détaillée et une démonstration du projet, regardez notre interview réalisée lors de l'événement :

➡️ **[https://www.youtube.com/embed/4ePYmL89ZWU?si=N-tWcXXGohGU8Tpc&amp;start=68)**

_(Retrouvez-moi dans la vidéo !)_

## Équipe

*   Andrew Assef
*   Matteo Khan
*   David Soeiro-Vuong
