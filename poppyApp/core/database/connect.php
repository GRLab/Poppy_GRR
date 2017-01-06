<?php

class Connexion{
	
	public static $oConnexion;

	/**
	 * Fonction de connexion à la base
	 */
	private static function connected(){
		$dsn = 'mysql:host=localhost;dbname=ProjetKERAAL;charset=utf8';
		$utilisateur = 'root';
		$motdepasse = 'ilovepoppy';
		try {
			self::$oConnexion = new PDO($dsn, $utilisateur , $motdepasse);
		} catch (PDOException $exception) {
			echo 'La connexion à la base de données a échouée : ', $exception -> getMessage();
			die; 
		}
	}
	
	/**
	 * Instanciation, utilisé pour se servir dans la base avant une requête
	 * @return PDO
	 */
	public static function getInstance(){
		if(!(self::$oConnexion instanceof PDO)){
			Connexion::connected();
		}
		return self::$oConnexion;
	}
}


?>