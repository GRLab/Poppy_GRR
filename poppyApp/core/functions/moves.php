<?php


if(isset($_GET["action"])){
	include '../database/connect.php';
	
	if($_GET["action"] == "insert"){
		insertMoveList($_POST["moveName"], $_POST["moveType"], $_POST["parts"]);
		echo  json_encode($_POST["moveName"]." saved in the database");
	} else if ($_GET["action"] == "insertMov"){
		//Il faut récupérer la liste des parties utilisées pour le mouvement (ou le sous mvt)
		$aParts = getPartsFichiers($_POST["listeFiles"]);
		//Et après on peut enregistrer
		insertMoveList($_POST["moveName"], $_POST["moveType"], $aParts);
		echo  json_encode($_POST["moveName"]." added to the database");
	} else if ($_GET["action"] == "symetry"){
		$changed = doSymetry($_POST["moveName"]);
		echo  json_encode(" symetry ok for ".$_POST["moveName"]);
	}else if ($_GET["action"] == "rename"){
		$changed = doRename($_POST["ancienNom"], $_POST["nouveauNom"]);
		echo  json_encode(" rename of ".$_POST["ancienNom"]." in ".$_POST["nouveauNom"].": ".$changed);
	} else if($_GET["action"] == "deleteMov"){
		deleteMove($_POST["moveName"]);
		echo  json_encode("removed");
	} else if ($_GET["action"] == "majBdD"){
		majBdd($_POST["listeMov"]);
		echo  json_encode("Database updated");
	} else if ($_GET["action"] == "insertJson"){
		insertJson($_POST["moveName"], $_POST["jsondata"], $_POST["nb_temps"]);
		echo  json_encode("json added into the database");
	} else if ($_GET["action"] == "checkJson"){
		$namelist = checkJson();
		echo  json_encode($namelist);
	} else if ($_GET["action"] == "getMovelist"){
		$movelist = getMovelist();
		echo  json_encode($movelist);
	} else if ($_GET["action"] == "getMovesNumber"){
		header('Content-type: application/json');
		$movesNumber = getMovesNumber();
		echo  json_encode($movesNumber);
	} else if ($_GET["action"] == "getTimeMov"){
		$iTime = getTimeMov($_POST["movename"]);
		echo $iTime;
	} else if ($_GET["action"] == "getInstructions"){
		header('Content-type: application/json');
		$aInstructions = getInstructions();
		echo json_encode($aInstructions);
	} else if ($_GET["action"] == "addInstruction"){
		addInstruction($_POST);
		echo json_encode("Added instruction");
	}
}

function doRename($previousName, $newName){
	$sSQL = "UPDATE `movelist` 
			 SET `moveName`= :newName
			 WHERE `moveName` = :previousName";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	$requete->execute(
						array('previousName' => $previousName, 'newName' => $newName)
					 );
	$changed = "ok";
	return $changed;
}

function doSymetry($sNameMov){
	// realise la symetrie des poppyParts
	$poppyParts = getPartsFichiers(array($sNameMov));
	if(in_array("bras_gauche", $poppyParts)==true && in_array("bras_droit", $poppyParts)==false){
		$sSQL = "UPDATE `movelist` 
				 SET `bras_gauche`=0, `bras_droit`=1
				 WHERE `moveName` = :moveName";
				 
		$requete = Connexion::getInstance()->prepare($sSQL);
		$requete->execute(
							array('moveName' => $sNameMov)
						 );
		$changed = "changed";
	} else if (in_array("bras_gauche", $poppyParts)==false && in_array("bras_droit", $poppyParts)==true){
		$sSQL = "UPDATE `movelist` 
				 SET `bras_gauche`=1, `bras_droit`=0
				 WHERE `moveName` = :moveName";
				 
		$requete = Connexion::getInstance()->prepare($sSQL);
		$requete->execute(
							array('moveName' => $sNameMov)
						 );
		$changed = "changed";
	}
	if(in_array("jambe_gauche", $poppyParts)==true && in_array("jambe_droite", $poppyParts)==false){
		$sSQL = "UPDATE `movelist` 
				 SET `jambe_gauche`=0, `jambe_droite`=1
				 WHERE `moveName` = :moveName";
				 
		$requete = Connexion::getInstance()->prepare($sSQL);
		$requete->execute(
							array('moveName' => $sNameMov)
						 );
		$changed = "changed";
	} else if (in_array("jambe_gauche", $poppyParts)==false && in_array("jambe_droite", $poppyParts)==true){
		$sSQL = "UPDATE `movelist` 
				 SET `jambe_gauche`=1, `jambe_droite`=0
				 WHERE `moveName` = :moveName";
				 
		$requete = Connexion::getInstance()->prepare($sSQL);
		$requete->execute(
							array('moveName' => $sNameMov)
						 );
		$changed = "changed";
	}  
	return $poppyParts;
}

function insertMoveList($sNameMov, $sMoveType, $aParts){
	
	//$sMoveType à remplacer par l'id quand on aura une liste déroulante, là ça fait une requête en plus pour récupérer l'id du type du mouvement
	
	$sSQL = "SELECT `id_moveType`
			 FROM `movetype`
			 WHERE `moveType` = :moveType";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	$requete->execute(
						array('moveType' => $sMoveType)
					 );

	$aDatas = $requete->fetchAll( PDO::FETCH_ASSOC);

	$iIDMoveType = $aDatas[0]["id_moveType"];
	
	$sParts = ",".implode(",", $aParts);
	
	$sAjout = "";
	for($i =0; $i < count($aParts); $i++){
		$sAjout.=",1";
	}
	$sSQL = "INSERT INTO `movelist`(moveName, id_moveType".$sParts.")
			 VALUES (:moveName, :moveType".$sAjout.")";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	
	$aArray = array("moveName" => $sNameMov, "moveType" => $iIDMoveType);
	
	$requete->execute($aArray);

	//MAJ nombre du type du mouvement ajouté à la BDD
	$sSQL = "UPDATE `movetype` 
			 SET `nb_movetype`=`nb_movetype`+1
			 WHERE `id_moveType` = :id_moveType";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	$requete->execute(
						array('id_moveType' => $iIDMoveType)
					 );
}

function insertJson($moveName, $jsondata, $nb_temps){
	$sSQL = "UPDATE `movelist` 
			 SET `nb_temps`= :nb_temps, `jsondata` = :jsondata
			 WHERE `moveName` = :moveName";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	$requete->execute(
						array('nb_temps' => $nb_temps, 'moveName' => $moveName, 'jsondata' => json_encode($jsondata))
					 );
}

function getPartsFichiers($aFiles){
	//On doit parcourir la liste de fichiers (qui sont enregistrés dans la base normalement)
	//Pour récupérer les parties influencées par ce mouvement.
	//Ensuite, en concaténant toutes les parties, on aura la liste des parties bougées pour ce mouvement
	$aParties = array();
	$aDatas = array();
	
	$sSQL = "SELECT * 
			 FROM `movelist`
			 WHERE `moveName` = :moveName";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	
	//On parcourt tous les fichiers
	foreach($aFiles as $sFile){
		$requete->execute(
						array('moveName' => $sFile)
				);
		
		$aDatas = $requete->fetch( PDO::FETCH_ASSOC);
		
		//On parcourt le résultat
		foreach($aDatas as $sKey => $aData){
			//On veut que la partie soit égale à 1, mais pas que ça soit l'id_move ou l'id_moveType
			if($aData == 1 && $sKey != "id_move" && $sKey != "id_moveType"){
				if(!in_array($sKey, $aParties)){
					$aParties[] = $sKey;
				}
				
			}
		}
	}

	return $aParties;
}

function deleteMove($sNameMov){
	$sSQL = "UPDATE `movetype` 
			 SET `nb_movetype`=`nb_movetype`-1
			 WHERE `id_moveType` = (SELECT `id_moveType` FROM `movelist` 
								WHERE `moveName` = :moveName)";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	$requete->execute(
						array('moveName' => $sNameMov)
					 );
	
	$sSQL = "DELETE FROM `movelist`
			 WHERE `moveName` = :moveName";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	$requete->execute(
						array('moveName' => $sNameMov)
					 );
}

function majBdd($aFiles){
	//On parcourt la liste, et on regarde si le mouvement (ou exo ou séance) est déjà dans la base
	//Si ce n'est pas le cas, alors on l'ajoute
	
	foreach ($aFiles as $sKey => $aFile){

		if(strstr($sKey, "list_")){//Si la clef contient "list_", c'est que c'est une clef qu'on veut
			$sKey = substr($sKey, 5); //On enl-ve le "list_" pour avoir que le nom qui nous intéresse
			
			//On parcourt les mouvements de chaque type (move, ss_mov, ss_mov_part, exo, seance)
			foreach($aFile as $sK => $aF){
				$bExist = checkIfExists($sK);
				
				//S'il n'existe pas, on l'insère dans la base
				if(!$bExist){
					insertMoveList($sK, $sKey, $aF);
				}
			}
		}
	}
	//MAJ du nombre de chaque type de mouvements
	majNbType();
}

function majNbType(){
	$sSQL = "UPDATE `movetype` 
			 SET `nb_movetype`=(SELECT COUNT(*) FROM `movelist` WHERE `id_moveType` = :idType)
			 WHERE `id_moveType` = :idType";

	for ($i = 1; $i <= 3; $i++){
		$requete = Connexion::getInstance()->prepare($sSQL);
		$requete->execute(
			array('idType' => $i)
		);
	}
}

function checkIfExists($sKey){
	$sSQL = "SELECT *
			 FROM `movelist`
			 WHERE `moveName` = :moveName";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);

	$requete->execute(
					array('moveName' => $sKey)
			);
			
	$aDatas = $requete->fetch( PDO::FETCH_ASSOC);
	
	if($aDatas){
		return true;
	} else {
		return false;
	}
}

function checkJson(){
	$sSQL = "SELECT `moveName`
			 FROM `movelist`
			 WHERE `nb_temps` IS NULL";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);

	$requete->execute();
			
	$aDatas = $requete->fetchAll( PDO::FETCH_ASSOC);
	
	return $aDatas;
}

function getMovelist(){
	$sSQL = "SELECT *
			 FROM `movelist`
			 ORDER BY `moveName`";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);

	$requete->execute();
			
	$aDatas = $requete->fetchAll( PDO::FETCH_ASSOC);
	
	return $aDatas;
}

function getMovesNumber(){
	$sSQL = "SELECT `nb_movetype`
			 FROM `movetype`
			 WHERE `id_moveType` = :id_moveType";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	for ($nb=1; $nb<=3; $nb++){
		$requete->execute(
						array('id_moveType' => $nb)
				);
			
		$movesNumber[$nb-1] = $requete->fetch( PDO::FETCH_ASSOC)["nb_movetype"];
	}

	return $movesNumber; 
}

function getTimeMov($sMove){
	$sSQL = "SELECT `nb_temps`
			 FROM `movelist`
			 WHERE `moveName` = :movename";

	$requete = Connexion::getInstance()->prepare($sSQL);

	$requete->execute(array("movename" => $sMove));
			
	$aDatas = $requete->fetch( PDO::FETCH_ASSOC);
	
	return $aDatas["nb_temps"];
}

function getInstructions(){
	$sSQL = "SELECT * 
	         FROM `instructions`
	         ORDER BY `description`";

	$requete = Connexion::getInstance()->prepare($sSQL);

	$requete->execute();
			
	$aDatas = $requete->fetchAll( PDO::FETCH_ASSOC);

	return $aDatas;
}

function addInstruction($aDatas){
	$sSQL = "INSERT INTO `instructions`(`title`,`description`,`voice`)
	         VALUES(:title, :description, :voice)";

	$requete = Connexion::getInstance()->prepare($sSQL);
	
	$requete->execute($aDatas);
}

?>
