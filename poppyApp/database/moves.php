<?php



if(isset($_GET["action"])){
	include '../database/connect.php';
	
	if($_GET["action"] == "insert"){
		insertMoveList($_POST["moveName"], $_POST["moveType"], $_POST["parts"]);
		echo  json_encode($_POST["moveName"]." saved in the database");
	} else if ($_GET["action"] == "insertMov"){
		//Il faut r�cup�rer la liste des parties utilis�es pour le mouvement (ou le sous mvt)
		$aParts = getPartsFichiers($_POST["listeFiles"]);
		//Et apr�s on peut enregistrer
		insertMoveList($_POST["moveName"], $_POST["moveType"], $aParts);
		echo  json_encode($_POST["moveName"]." added to the database");
	} else if($_GET["action"] == "deleteMov"){
		deleteMove($_POST["moveName"]);
		echo  json_encode("removed");
	} else if ($_GET["action"] == "majBdD"){
		majBdd($_POST["listeMov"]);
		echo  json_encode("Database updated");
	}
	
}


function insertMoveList($sNameMov, $sMoveType, $aParts){
	
	//$sMoveType � remplacer par l'id quand on aura une liste d�roulante, l� �a fait une requ�te en plus pour r�cup�rer l'id du type du mouvement
	
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
} 

function getPartsFichiers($aFiles){
	//On doit parcourir la liste de fichiers (qui sont enregistr�s dans la base normalement)
	//Pour r�cup�rer les parties influenc�es par ce mouvement.
	//Ensuite, en concat�nant toutes les parties, on aura la liste des parties boug�es pour ce mouvement
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
		
		//On parcourt le r�sultat
		foreach($aDatas as $sKey => $aData){
			//On veut que la partie soit �gale � 1, mais pas que �a soit l'id_move ou l'id_moveType
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
	$sSQL = "DELETE FROM `movelist`
			 WHERE `moveName` = :moveName";
			 
	$requete = Connexion::getInstance()->prepare($sSQL);
	$requete->execute(
						array('moveName' => $sNameMov)
					 );
}

function majBdd($aFiles){
	//On parcourt la liste, et on regarde si le mouvement (ou exo ou s�ance) est d�j� dans la base
	//Si ce n'est pas le cas, alors on l'ajoute
	
	foreach ($aFiles as $sKey => $aFile){

		if(strstr($sKey, "list_")){//Si la clef contient "list_", c'est que c'est une clef qu'on veut
			$sKey = substr($sKey, 5); //On enl-ve le "list_" pour avoir que le nom qui nous int�resse
			
			//On parcourt les mouvements de chaque type (move, ss_mov, ss_mov_part, exo, seance)
			foreach($aFile as $sK => $aF){
				$bExist = checkIfExists($sK);
				
				//S'il n'existe pas, on l'ins�re dans la base
				if(!$bExist){
					insertMoveList($sK, $sKey, $aF);
				}
			}
		}
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

?>