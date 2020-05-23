# Projet de Bases de Données Relationnelles - M1DS

## Composition du groupe 
Chiara CORDIER et Nolwenn DAVID

## Sujet envisagé
**ETUDE DES ACCIDENTS D'AVION** --> on essaiera de créer un site pour pouvoir rechercher des informations sur ces accidents en fonction des lieux, des compagnies, des types d'avion, et des années

## Etat actuel de la réalisation du projet
 - [x] création du projet sur django
 - [x] récupération et nettoyage des données
 - [x] création du modèle de la base
 - [x] peuplement de la base
 - [x] création des pages du site
 - [x] page d'administration
  
## Description des fichiers du dépôt
 - blog.txt : idées, problèmes et réalisations au jour le jour

 - projet_BDR : dossier du projet créé avec django

 - recup_data.py : pour récupérer et nettoyer des données du site https://openflights.org/data.html
 - aeroport.csv, avion.csv, compagnie.csv, pays.csv : fichiers des données récupérées et nettoyées du site https://openflights.org/data.html

 - Recup_accidents.py : pour récupérées et nettoyées les données du site http://aviation-safety.net/
 - Donnees_accidents.csv : données récupérées et nettoyées du site http://aviation-safety.net/

 - organisation_base.pdf : organisation des tables de notre base (avec son évolution)
 - peuplement_tables.py : pour peupler la base
 
## Etat de la récupération des données, du nettoyage et de la mise en forme
 - [x] récupération
 - [x] nettoyage
 - [x] modifications pour cohérence entre les tables 
  
## Etat de la base de données réalisée
 - [x] remplissage de toutes les tables
    
## Programmes réalisés et fonctionnalités opérationnelles
 - [x] création de pages pour afficher nos données
 - [x] page d'accueil
 - [x] tableaux de recherche dans chaque page
 - [x] page des accidents : 
	* tableau de recherche
	* options pour croiser, regrouper, interroger les données
	* affichage de graphes
	* options de tri
 - [ ] graphiques pour avoir une vue d'ensemble des accidents

