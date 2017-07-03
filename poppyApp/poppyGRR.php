<?php 
session_start();
//error_reporting(0);
require 'core/database/connect.php';
$errors = array();
include 'core/functions/moves.php';
//include 'includes/overall/overallheader.php'; 
include "includes/head.php";


?>
<body onload="initPage()">

<?php
include "includes/header.php";
?>


<div id="container">

<!--partie boutons-->
	<div id='application'>
		<div id="movelist">
		</div>
		<!-- TODO !!!!!!!!!! -->
		<div id="boutons">
			<div id="poppy">
				<img src="includes/images/notconnected.png" id="poppyConnected" alt="Statut connection">
				Poppy : 
				<input value="" id="poppyName" onchange="majPoppyName()">
				<span id="temperatureMax"></span><span id="tempMax">Tmax :</span> 
			</div>
			<br>
			<div class="power">
			<div class="title2">Alimentation</div>
			<table id="compliantTable"> 
			<tr id="firstLine">
				<td style="font-weight:bold;" id="compliantPart">Tous les moteurs </td>
				<td><input id='compliant' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini" data-height="15"></td>
				<td class="semiMou">semi-mou</td>
			</tr>
			<tr class="compliantRow">
				<td id="compliantPartT">Tete</td>
				<td><input id='compliantT' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini"> </td>
				<td class="semiMou"><input type="checkbox" id='semiMouT' name="poppyPartsMou" value="tete" ></td>
			</tr>
			<tr class="compliantRow">
				<td id="compliantPartBG">BrasG</td> 
				<td><input id='compliantBG' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini"> </td>
				<td class="semiMou"><input type="checkbox" id='semiMouBG' name="poppyPartsMou" value="bras_gauche"></td>
			</tr>
			<tr class="compliantRow">
				<td id="compliantPartBD">BrasD</td>
				<td><input id='compliantBD' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini"> </td>
				<td class="semiMou"><input type="checkbox" id='semiMouBD' name="poppyPartsMou" value="bras_droit" ></td>
			</tr>
			<tr class="compliantRow">
				<td id="compliantPartCol">Colonne </td>
				<td><input id='compliantCol' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini"> </td>
				<td class="semiMou"><input type="checkbox" id='semiMouCol' name="poppyPartsMou" value="colonne"></td>
			</tr>
			<tr class="compliantRow">
				<td id="compliantPartJG">JambeG </td>
				<td><input id='compliantJG' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini"> </td>
				<td class="semiMou"><input type="checkbox" id='semiMouJG' name="poppyPartsMou" value="jambe_gauche"></td>
			</tr>
			<tr class="compliantRow">
				<td id="compliantPartJD">JambeD </td>
				<td><input id='compliantJD' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini"> </td>
				<td class="semiMou"><input type="checkbox" id='semiMouJD' name="poppyPartsMou" value="jambe_droite"></td>
			</tr>

			</table>
			<br><div> <span id="titlePosition">Position initiale :</span> 
				<input type="button" value="debout" onclick='GoDebout()' id='goDebout' /> 
				<input type="button" value="chaise" onclick='GoChaise()' id='goChaise' /> 
				<input type="button" value="assis" onclick='GoAssis()' id='goAssis' /><br> 
				</div>
			</div>
			
			<div class="poppyimage">
				<img src="includes/images/poppyImage.png" id="poppyImage" alt ="PoppyImage"  class="map" usemap="#simple" > 
			</div>
			<div class="save">
			<div class="title2">Enregistrement</div>
			<input type="button" value="enregistrer mouvement" id='SavSsMovePart' data-toggle="modal" data-target="#modal_create_ss_mvt_part" /> <br>
			<input type="button" value="creer mouvement" id='createMove' data-toggle="modal" data-target="#modal_create_mov" /> <br>
			<input type="button" value="creer exercice" id='createExo' data-toggle="modal" data-target="#modal_create_exo"/> <br>
			<input type="button" value="creer seance" id='createSeance' data-toggle="modal" data-target="#modal_create_seance"/> <br>
			</div>
			<!--input type="button" value="save init pos" onclick='SaveInitPos()' id='saveinitpos' /><br> <br--> 
			<!--input type="button" value="receive movefile" onclick="ReceiveFile()" id='Datareceive'/> <br> <br-->
		</div>

	 	<!--suivi avancement exercice/seance en cours-->
		<div id='exoConfig'>
			<div id="progressbar"></div>
			<div id="progressbarlabel"></div>
		</div>
	</div>
	<div id="contenu">
		<input type="button" value="Mettre à jour le robot" id="majPoppy" onclick="majPoppy()" />
		<input type="button" value="Mettre à jour la base" id="majBdD" onclick="majBdD()" />
		<input type="button" value="volume" id="volume" onclick="setRobotVolume()" />
		<input type="button" value="faceState" id="faceStateBtn"  data-toggle="modal" data-target="#modal_setFaceState" />
		<input type="button" value="EyesDirection" id="EyesDirectionBtn" data-toggle="modal" data-target="#modal_setEyesDirection" />
		<input type="button" value="Eteindre Poppy" id="stopPoppy" onclick="stopPoppy()" />
		<br><br>
	</div>
</div>

<map name="simple">

	<!-- Zone grise -->

	<area shape="poly" id="actif_T" data-maphilight='{"stroke":false,"fillColor":"000000","fillOpacity":0.4, "neverOn": true, "alwaysOn" : true}' coords="109,5,82,7,96,6,96,5,113,6,113,6,122,6,122,7,127,7,132,11,138,19,138,41,136,39,136,42,135,44,133,48,130,50,126,53,122,54,122,53,121,53,120,54,114,55,114,59,111,59,111,61,95,61,92,59,91,53,85,53,81,52,76,51,72,45,72,17,74,13,85,6,86,6" alt="" />

 	<area shape="poly" id="actif_BG" data-maphilight='{"stroke":false,"fillColor":"000000","fillOpacity":0.4, "neverOn": true,"alwaysOn" : true}' coords="140,68,141,69,161,69,164,71,164,76,163,83,166,85,166,86,164,87,165,94,166,98,167,104,168,111,168,126,171,135,173,143,173,156,174,156,174,162,176,162,176,178,176,225,175,235,171,239,169,239,166,234,170,228,170,214,168,212,164,221,161,221,161,216,161,212,162,211,162,206,165,201,165,198,165,194,165,194,160,175,151,155,149,154,151,145,150,146,149,121,149,121,149,116,148,116,147,108,146,109,146,95,143,95,143,86,144,86,145,82,138,82,138,68,144,69" alt="" />

 	<area shape="poly" id="actif_BD" data-maphilight='{"stroke":false,"fillColor":"000000","fillOpacity":0.4, "neverOn": true,"alwaysOn" : true}' coords="48,65,50,65,57,65,58,66,66,67,65,80,62,80,61,82,61,86,59,90,59,97,54,121,51,138,46,157,46,162,43,163,33,179,26,196,26,216,25,217,20,211,21,221,20,232,17,232,17,233,14,233,12,209,21,173,21,164,28,134,31,128,38,89,40,81,42,69,48,65"alt="" />

 	<area shape="poly" id="actif_Col" data-maphilight='{"stroke":false,"fillColor":"000000","fillOpacity":0.4, "neverOn": true,"alwaysOn" : true}' coords="66,63,67,65,77,63,77,64,83,65,87,65,92,63,96,63,97,60,98,58,110,58,110,60,113,60,114,62,122,65,138,65,139,66,139,69,139,86,125,89,123,90,113,94,113,128,114,131,118,132,118,147,113,147,113,151,115,151,116,153,117,155,116,158,118,158,117,163,123,165,123,178,122,179,121,179,121,183,119,185,117,186,115,188,101,188,101,184,98,184,98,185,97,185,97,189,86,189,82,188,82,178,75,178,75,163,81,165,87,159,87,150,88,150,88,146,92,146,91,144,90,143,90,142,85,136,86,131,91,130,90,124,90,95,85,90,81,89,66,84,66,64,70,64" alt="" />

 	<area shape="poly" id="actif_JG" data-maphilight='{"stroke":false,"fillColor":"000000","fillOpacity":0.4, "neverOn": true,"alwaysOn" : true}' coords="124,162,125,162,143,163,142,170,142,175,140,176,140,179,147,183,147,197,146,197,146,211,133,255,140,258,141,264,140,289,137,290,136,307,134,353,141,359,141,384,135,389,113,389,109,386,109,364,114,356,111,290,106,288,106,258,113,253,113,248,118,229,120,212,121,211,121,186,126,179,126,178,121,177,122,162,143,163"alt="" />

 	<area shape="poly" id="actif_JD" data-maphilight='{"stroke":false,"fillColor":"000000","fillOpacity":0.4, "neverOn": true,"alwaysOn" : true}' coords="59,161,60,162,74,160,76,163,76,177,73,179,78,182,81,194,85,243,86,254,92,256,92,272,86,328,84,355,89,361,88,376,85,388,57,388,55,378,55,370,64,354,62,289,57,287,59,254,64,253,64,248,52,207,53,177,59,173,59,162" alt="" />



 	<!-- Zone orange -->
 	<area shape="poly" id="actif_T_warning" data-maphilight='{"stroke":false,"fillColor":"F37413","fillOpacity":0.6, "neverOn": true, "alwaysOn" : false}' coords="109,5,82,7,96,6,96,5,113,6,113,6,122,6,122,7,127,7,132,11,138,19,138,41,136,39,136,42,135,44,133,48,130,50,126,53,122,54,122,53,121,53,120,54,114,55,114,59,111,59,111,61,95,61,92,59,91,53,85,53,81,52,76,51,72,45,72,17,74,13,85,6,86,6" alt="" />

 	 <area shape="poly" id="actif_BG_warning" data-maphilight='{"stroke":false,"fillColor":"F37413","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}'  coords="140,68,141,69,161,69,164,71,164,76,163,83,166,85,166,86,164,87,165,94,166,98,167,104,168,111,168,126,171,135,173,143,173,156,174,156,174,162,176,162,176,178,176,225,175,235,171,239,169,239,166,234,170,228,170,214,168,212,164,221,161,221,161,216,161,212,162,211,162,206,165,201,165,198,165,194,165,194,160,175,151,155,149,154,151,145,150,146,149,121,149,121,149,116,148,116,147,108,146,109,146,95,143,95,143,86,144,86,145,82,138,82,138,68,144,69" href="#" alt="" />

 	<area shape="poly" id="actif_BD_warning" data-maphilight='{"stroke":false,"fillColor":"F37413","fillOpacity":0.8, "neverOn": true,"alwaysOn" : false}' coords="48,65,50,65,57,65,58,66,66,67,65,80,62,80,61,82,61,86,59,90,59,97,54,121,51,138,46,157,46,162,43,163,33,179,26,196,26,216,25,217,20,211,21,221,20,232,17,232,17,233,14,233,12,209,21,173,21,164,28,134,31,128,38,89,40,81,42,69,48,65" alt="" />

 	<area shape="poly" id="actif_Col_warning" data-maphilight='{"stroke":false,"fillColor":"F37413","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}'  coords="66,63,67,65,77,63,77,64,83,65,87,65,92,63,96,63,97,60,98,58,110,58,110,60,113,60,114,62,122,65,138,65,139,66,139,69,139,86,125,89,123,90,113,94,113,128,114,131,118,132,118,147,113,147,113,151,115,151,116,153,117,155,116,158,118,158,117,163,123,165,123,178,122,179,121,179,121,183,119,185,117,186,115,188,101,188,101,184,98,184,98,185,97,185,97,189,86,189,82,188,82,178,75,178,75,163,81,165,87,159,87,150,88,150,88,146,92,146,91,144,90,143,90,142,85,136,86,131,91,130,90,124,90,95,85,90,81,89,66,84,66,64,70,64" alt="" />

 	<area shape="poly" id="actif_JG_warning" data-maphilight='{"stroke":false,"fillColor":"F37413","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}' coords="124,162,125,162,143,163,142,170,142,175,140,176,140,179,147,183,147,197,146,197,146,211,133,255,140,258,141,264,140,289,137,290,136,307,134,353,141,359,141,384,135,389,113,389,109,386,109,364,114,356,111,290,106,288,106,258,113,253,113,248,118,229,120,212,121,211,121,186,126,179,126,178,121,177,122,162,143,163" alt="" />

 	<area shape="poly" id="actif_JD_warning" data-maphilight='{"stroke":false,"fillColor":"F37413","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}' coords="59,161,60,162,74,160,76,163,76,177,73,179,78,182,81,194,85,243,86,254,92,256,92,272,86,328,84,355,89,361,88,376,85,388,57,388,55,378,55,370,64,354,62,289,57,287,59,254,64,253,64,248,52,207,53,177,59,173,59,162" alt="" />



 	<!-- Zone rouge -->
 	<area shape="poly" id="actif_T_stop" data-maphilight='{"stroke":false,"fillColor":"EC0000","fillOpacity":0.6, "neverOn": true, "alwaysOn" : false}' coords="109,5,82,7,96,6,96,5,113,6,113,6,122,6,122,7,127,7,132,11,138,19,138,41,136,39,136,42,135,44,133,48,130,50,126,53,122,54,122,53,121,53,120,54,114,55,114,59,111,59,111,61,95,61,92,59,91,53,85,53,81,52,76,51,72,45,72,17,74,13,85,6,86,6" alt="" />

 	<area shape="poly" id="actif_BG_stop" data-maphilight='{"stroke":false,"fillColor":"EC0000","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}' coords="140,68,141,69,161,69,164,71,164,76,163,83,166,85,166,86,164,87,165,94,166,98,167,104,168,111,168,126,171,135,173,143,173,156,174,156,174,162,176,162,176,178,176,225,175,235,171,239,169,239,166,234,170,228,170,214,168,212,164,221,161,221,161,216,161,212,162,211,162,206,165,201,165,198,165,194,165,194,160,175,151,155,149,154,151,145,150,146,149,121,149,121,149,116,148,116,147,108,146,109,146,95,143,95,143,86,144,86,145,82,138,82,138,68,144,69" alt="" />

 	<area shape="poly" id="actif_BD_stop" data-maphilight='{"stroke":false,"fillColor":"EC0000","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}' coords="48,65,50,65,57,65,58,66,66,67,65,80,62,80,61,82,61,86,59,90,59,97,54,121,51,138,46,157,46,162,43,163,33,179,26,196,26,216,25,217,20,211,21,221,20,232,17,232,17,233,14,233,12,209,21,173,21,164,28,134,31,128,38,89,40,81,42,69,48,65" alt="" />

 	<area shape="poly" id="actif_Col_stop" data-maphilight='{"stroke":false,"fillColor":"EC0000","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}' coords="66,63,67,65,77,63,77,64,83,65,87,65,92,63,96,63,97,60,98,58,110,58,110,60,113,60,114,62,122,65,138,65,139,66,139,69,139,86,125,89,123,90,113,94,113,128,114,131,118,132,118,147,113,147,113,151,115,151,116,153,117,155,116,158,118,158,117,163,123,165,123,178,122,179,121,179,121,183,119,185,117,186,115,188,101,188,101,184,98,184,98,185,97,185,97,189,86,189,82,188,82,178,75,178,75,163,81,165,87,159,87,150,88,150,88,146,92,146,91,144,90,143,90,142,85,136,86,131,91,130,90,124,90,95,85,90,81,89,66,84,66,64,70,64" alt="" />

 	<area shape="poly" id="actif_JG_stop" data-maphilight='{"stroke":false,"fillColor":"EC0000","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}' coords="124,162,125,162,143,163,142,170,142,175,140,176,140,179,147,183,147,197,146,197,146,211,133,255,140,258,141,264,140,289,137,290,136,307,134,353,141,359,141,384,135,389,113,389,109,386,109,364,114,356,111,290,106,288,106,258,113,253,113,248,118,229,120,212,121,211,121,186,126,179,126,178,121,177,122,162,143,163" alt="" />

 	<area shape="poly" id="actif_JD_stop" data-maphilight='{"stroke":false,"fillColor":"EC0000","fillOpacity":0.6, "neverOn": true,"alwaysOn" : false}' coords="59,161,60,162,74,160,76,163,76,177,73,179,78,182,81,194,85,243,86,254,92,256,92,272,86,328,84,355,89,361,88,376,85,388,57,388,55,378,55,370,64,354,62,289,57,287,59,254,64,253,64,248,52,207,53,177,59,173,59,162" alt="" />

</map>

	<script>

		function putHighlight(id){
			var data = $(id).data('maphilight') || {};
            data.alwaysOn = !data.alwaysOn;
            $(id).data('maphilight', data).trigger('alwaysOn.maphilight');
		}

	    $(function() {

	    	$('.map').maphilight();

		    $('#compliant').change(function() {
		    	
		    	Compliant();
		    });
		    $('#semiMouT').change(function() {
		        PartNonCompliant();
		    });

		    $('#semiMouBG').change(function() {
		        PartNonCompliant();
		    });

		    $('#semiMouBD').change(function() {
		      	PartNonCompliant();
		    });

		    $('#semiMouCol').change(function() {
		        PartNonCompliant();
		    });

		    $('#semiMouJG').change(function() {
		        PartNonCompliant();
		    });

		    $('#semiMouJD').change(function() {
		        PartNonCompliant();
		    });

		    $('#compliantT').change(function() {
		    	!checkActiveArea("T") ? putHighlight("#actif_T") : "";
		      	PartNonCompliant();
		    });

		    $('#compliantBG').change(function() {
		    	!checkActiveArea("BG") ? putHighlight("#actif_BG") : "";
		        PartNonCompliant();
		    });

		    $('#compliantBD').change(function() {
		    	!checkActiveArea("BD") ? putHighlight("#actif_BD") : "";
		      	PartNonCompliant();
		    });

		    $('#compliantCol').change(function() {
		    	!checkActiveArea("Col") ? putHighlight("#actif_Col") : "";
		        PartNonCompliant();
		    });

		    $('#compliantJG').change(function() {
		    	!checkActiveArea("JG") ? putHighlight("#actif_JG") : "";
		     	PartNonCompliant();
		    });

		    $('#compliantJD').change(function() {
		    	!checkActiveArea("JD") ? putHighlight("#actif_JD") : "";
		      	PartNonCompliant();
		    });
	    });

	  //END TODO
	</script>

	<!-- Modal -->
	<div class="modal fade" id="modal_setFaceState" role="dialog">
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Expression du robot <span id="ancienNom"></span></h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<label for="newName">Nouvel état : </label> 
					<select id="faceState">
						<option value="happy">normal</option>
						<option value="angry">angry</option>
						<option value="forcing">forcing</option>
						<option value="asleep">asleep</option>
						<option value="dead">dead</option>
						<option value="bored">bored</option>
						<option value="confused">confused</option>
						<option value="sad">sad</option>
					</select>
				</fieldset>
			</div>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
			  <button type="button" class="btn btn-info" onclick="setFaceState()">Envoyer</button>
			</div> 
		  </div>
		</div>
	</div>

	<div class="modal fade" id="modal_setEyesDirection" role="dialog">
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Direction des yeux<span id="ancienNom"></span></h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<label for="newName">Nouvelle direction : </label> 
					<select id="eyesDirection">
						<option value="topleft">topleft</option>
						<option value="top">top</option>
						<option value="topright">topright</option>
						<option value="left">left</option>
						<option value="center">center</option>
						<option value="right">right</option>
						<option value="bottomleft">bottomleft</option>
						<option value="bottom">bottom</option>
						<option value="bottomright">bottomright</option>
					</select>
				</fieldset>
			</div>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Annuler</button>
			  <button type="button" class="btn btn-info" onclick="setEyesDirection()">Envoyer</button>
			</div> 
		  </div>
		</div>
	</div>

	<div class="modal fade" id="modal_rename" role="dialog">
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Renommer <span id="ancienNom"></span></h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<label for="newName">Nouveau nom</label> <input value="" type="text" class="form-control" id="newName" placeholder="Nouveau nom" />
				</fieldset>
			</div>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" onclick="RenameClear()" data-dismiss="modal">Annuler</button>
			  <button type="button" class="btn btn-info" onclick="RenameSuite()">Sauvegarder</button>
			</div> 
		  </div>
		</div>
	</div>

	<div class="modal fade" id="modal_create_ss_mvt_part" role="dialog">
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Sauvegarde une partie d'un sous mouvement</h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<div><label for="nom_mvt_ss_part">Nom du mouvement</label></div>
					<div class="tab_nom_save"><input type="text" class="input_shadow form-control" id="nom_mvt_ss_part" placeholder="nom du mouvement" /></div>
				</fieldset>
				<fieldset class="form-group">
					<div><label for="nom_playedMove">Nom du mouvement joué pendant la sauvegarde</label></div>
					<div class="tab_nom_save"><input type="text" class="input_shadow form-control" id="nom_playedMove" placeholder="nom du mouvement" /></div>
				</fieldset>
				<fieldset class="form-group">
					<label>Parties de Poppy qui vont être bougées</label>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsCreatePart" value="bras_gauche">Bras gauche</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsCreatePart" value="bras_droit">Bras droit</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsCreatePart" value="jambe_gauche">Jambe gauche</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsCreatePart" value="jambe_droite">Jambe droite</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsCreatePart" value="tete">Tête</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsCreatePart" value="colonne">Colonne</label>
					</div>
				</fieldset>
				<fieldset class="form-group">
					<div class="checkbox">
					  <label><input type="checkbox" name="semiMou" value="True">Mode semi-mou</label>
					</div>
				</fieldset>
			</div>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-info" onclick="SaveSsMovePart()">Sauvegarder</button>
			</div>
		  </div>
		</div>
	</div>

	<div class="modal fade" id="modal_create_mov" role="dialog">
		<div class="modal-dialog modal-lg">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Création d'un mouvement</h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<div><label for="nom_mov">Nom du mouvement</label></div>
					<div class="tab_nom"> <input type="text" class="input_shadow form-control" id="nom_mov" placeholder="nom du mouvement à creer" /></div>
				</fieldset>

				<!--partie dynamique pour ajouter un nombre n de ss_mov(_part) dans la fusion-->
				<table id="add_ss_mov">
					<tr>
						<td>
						<div><label for="nom_mov">sous-mouvement 1</label></div>
						<div class="tab_nom"><fieldset class="form-group">
							<input type="text" title="Nom du sous mouvement composant le mouvement." class="input_shadow form-control" id="ss_mov_1" placeholder="nom du mouvement" />
						</fieldset></div>
						<div class="tab_vit"><fieldset class="form-group">
							<input type="text" title="Vitesse de lecture du sous mouvement, comprise entre 1 et 10. Une vitesse 9 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible" class="input_shadow form-control" id="speed_1" placeholder="vitesse" />
						</fieldset></div>
						<div class="tab_pause"><fieldset class="form-group">
							<input type="text" title="Décalage temporel entre le début du mouvement et le début du sous mouvement. L'unité est l'incrément (environ 0.25s en vitesse normale, cette valeur augmente si la vitesse diminue). Plus l'offset est grand, et plus le mouvement démarrera avec du retard." class="input_shadow form-control" id="offset_1" placeholder="offset" />
						</fieldset></div>
						<!--td class="pull-right"><fieldset class="form-group"><button title="Supprimer la ligne" class="btn btn-danger supp_ligne"><span class="glyphicon glyphicon-trash" ></span></button></fieldset></td-->
						</td>
					</tr>
				</table>
				<button type="button" class="btn btn-info" onclick="add_one_ss_mov()">Ajouter</button>
			</div>

			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-default" onclick="PrevisualisationMove()">Prévisualiser</button>
			  <button type="button" class="btn btn-info" onclick="CreateMove()">Sauvegarder</button>
			</div>
		  </div>
		</div>
	</div>
	
	<div class="modal fade" id="modal_create_exo" role="dialog">
		<div class="modal-dialog modal-lg">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Création d'un exercice</h4>
			</div>
			<div class="modal-body">
				<div class="center"><img src="./includes/images/barre.png" class="barreInitiale" alt="barre"><img src="./includes/images/fleche.png" alt="fleche" class="fleche"><span class="spanTimeInitial">0</span></div>

				<fieldset class="form-group">
					<div><label for="nom_exo">Nom de l'exercice</label></div> 
					<div class="tab_nom"><input type="text" class="input_shadow form-control" id="nom_exo" placeholder="nom de l'exercice" /></div>
				</fieldset>

				<!--partie dynamique pour ajouter un nombre n de move dans la concatenation-->
				<table id="add_mov">
					<tr>
						<tr>
							<td colspan="3">
							<div><label for="type_exo">mouvement 1</label></div>
							<div class="tab_nom"><fieldset class="form-group">
								<input type="text" title="Nom du mouvement composant l'exercice à créer." class="input_shadow form-control mvt_timeline" id="mov_1" placeholder="nom du mouvement" />
							</fieldset></div>
							<div class="tab_vit"><fieldset class="form-group">
								<input type="text" title="Vitesse de lecture du mouvement, comprise entre 1 et 10. Une vitesse 5 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible" class="input_shadow form-control" id="speedmov_1" placeholder="vitesse" />
							</fieldset></div>
							<div class="tab_pause"><fieldset class="form-group">
								<input type="text" title="Correspond à la pause après le mouvement concerné. La pause est en secondes." class="input_shadow form-control pause_timeline" id="pausemov_1" placeholder="pause" />
							</fieldset></div>
							</td>
							<!--td class="pull-right"><fieldset class="form-group"><button title="Supprimer la ligne" class="btn btn-danger supp_ligne"><span class="glyphicon glyphicon-trash" ></span></button></fieldset></td-->
						</tr>
						<tr>
							<td id="add_voice_1" colspan="3">
							</td>
						</tr>
						<tr>
							<td colspan="3">
							<div class="tab_voix_vide"> </div>
							<div class="tab_voix_button"><button id="btn_mov_1" type="button" class="btn btn-info" onclick="add_one_voice('1')">Voix</button></div>
							</td>
						</tr>
					</tr>
				</table>
				<button type="button" class="btn btn-info" onclick="add_one_mov()">Ajouter</button>
			</div>

			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-info" onclick="CreateExo('exo')">Sauvegarder</button>
			</div>
		  </div>
		</div>
	</div>

	<div class="modal fade" id="modal_create_seance" role="dialog">
		<div class="modal-dialog modal-lg">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Création d'une séance</h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<div><label for="nom_seance">Nom de la séance</label></div> 
					<div class="tab_nom"><input type="text" class="input_shadow form-control" id="nom_seance" placeholder="nom de la séance" /></div>
				</fieldset>

				<!--partie dynamique pour ajouter un nombre n d'exercices dans la concatenation-->
				<table id="add_exo">
					<tr>
						<td colspan="3">
						<div><label for="type_exo">exercice 1</label></div>
						<div class="tab_nom"><fieldset class="form-group">
							<input type="text" title="Nom de l'exercice composant le fichier à créer." class="input_shadow form-control" id="exo_1" placeholder="nom de l'exercice" />
						</fieldset></div>
						<div class="tab_vit"><fieldset class="form-group">
							<input type="text" title="Vitesse de lecture de l'exercice, comprise entre 1 et 10. Une vitesse 5 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible" class="input_shadow form-control" id="speedexo_1" placeholder="vitesse" />
						</fieldset></div>
						<div class="tab_pause"><fieldset class="form-group">
							<input type="text" title="Correspond à la pause après l'exercice concerné. La pause est en secondes." class="input_shadow form-control" id="pauseexo_1" placeholder="pause" />
						</fieldset></div>
						</td>
							<!--td class="pull-right"><fieldset class="form-group"><button title="Supprimer la ligne" class="btn btn-danger supp_ligne"><span class="glyphicon glyphicon-trash" ></span></button></fieldset></td-->
					</tr>
				</table>
				<button type="button" class="btn btn-info" onclick="add_one_exo()">Ajouter</button>
			</div>

			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-info" onclick="CreateExo('seance')">Sauvegarder</button>
			</div>
		  </div>
		</div>
	</div>

	<div class="modal fade" id="modal_go_move" role="dialog">
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Jouer un mouvement</h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<label for="nom_mvt">Nom du mouvement</label> <input type="text" class="form-control" id="nom_mvt" placeholder="MoveName" />
				</fieldset>
				<fieldset class="form-group">
					<label for="speed">vitesse du mouvement [1 : low, 2: normal, 3: fast, 4: very fast]</label> <input type="text" class="form-control" id="speed" placeholder="2" />
				</fieldset>
				<fieldset class="form-group">
					<label>Parties de Poppy qui vont être bougées</label>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsGo" value="bras_gauche">Bras gauche</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsGo" value="bras_droit">Bras droit</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsGo" value="jambe_gauche">Jambe gauche</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsGo" value="jambe_droite">Jambe droite</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsGo" value="tete">Tête</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyPartsGo" value="colonne">Colonne</label>
					</div>
				</fieldset>
			</div>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-info" onclick="GoMove()">Play</button>
  			  <button type="button" class="btn btn-info" onclick="GoRev()">Play reverse</button>
			</div>
		  </div>
		</div>
	</div>
  
    <div class="modal fade" id="modal_part_non_compliant" role="dialog">
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Parties de Poppy</h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<label>Parties de Poppy </label>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyParts" value="bras_gauche">Bras gauche</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyParts" value="bras_droit">Bras droit</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyParts" value="jambe_gauche">Jambe gauche</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyParts" value="jambe_droite">Jambe droite</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyParts" value="tete">Tête</label>
					</div>
					<div class="checkbox">
					  <label><input type="checkbox" name="poppyParts" value="colonne">Colonne</label>
					</div>
				</fieldset>
			</div>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-info" onclick="PartNonCompliant()">Envoyer</button>
			</div>
		  </div>
		</div>
	</div>

	<script>
		var tabTime = [];
		$(function(){
			
			var progressbar = $( "#progressbar" );
	 
			progressbar.progressbar({
				value: 0
			});

			$(document).on('click', '.supp_ligne', function(){
				$(this).closest("tr").remove();
			});

			$(document).on('change', ".mvt_timeline", function(){
				input = $(this);
				$.post('./core/functions/moves.php?action=getTimeMov', {"movename" : $(this).val()}, function(data){
					id = $(input).attr('id');
					if(tabTime[id] != undefined){
						delete tabTime[id];
						delete tabTime["pause"+id];
					}
					if (data != undefined && data != 0){
						tabTime[id] = data;

						if($('#pause'+id).val() != ""){
							tabTime["pause"+id] = $('#pause'+id).val();
						} else {
							tabTime["pause"+id] = 0;
						}
					}

					majTimeline();
					
				});
			});

			$(document).on('change', '.pause_timeline', function(){
				tabTime[$(this).attr('id')] = $(this).val();
				majTimeline();
			});

			$(document).on('change', '.voice_time', function(){
				majVoiceTimeline();
			});

			$(document).on('change', '.voice_texte', function(){
				id=$(this).attr('id').split("_");
				id=id[2];	
				$('#span_voix_'+id).attr('title', $(this).val());
			});
		});

		function majVoiceTimeline(){
			var somme = 0;

			for (var key in tabTime){
				somme+= parseInt(tabTime[key]);
			}

			$('div.center span.spanVoix').remove();

			$('.voice_time').each(function(i,o){
				val_time = $(this).val();
				pos = (100*val_time)/somme;
				pos-=2;
				texte = "";

				id=$(this).attr('id').split("_");
				id=id[2];

				if($('#voice_texte_'+id).val() != "undefined")
					texte = $('#voice_texte_'+id).val();

				if (val_time < somme && val_time!="")
					$('div.center').append('<span class="spanVoix" id="span_voix_'+id+'" title="'+texte+'" style="left:'+pos+'%">'+id+'</span>');
			});
		}

		function majTimeline(){
			var somme = 0;

			for (var key in tabTime){
				somme+= parseInt(tabTime[key]);
			}

			//Somme => 100%
			//nb_increment => x %
			//x = (100*nb_increment)/somme  => résultat en %

			$('div.center img.barre').remove();
			$('div.center span.spanTime').remove();
			$('div.center span.spanMvt').remove();
			
			majVoiceTimeline();

			var sommeCumul= 0;
			var precPos = 0;

			for(i = 1; i < nb_mov +1; i++){
				if(tabTime["mov_"+i] != undefined){
					sommeCumul+= parseInt(tabTime["mov_"+i]);
					position = (100*sommeCumul)/somme;

					positionSpan = position - 1;

					if(sommeCumul >= 100)
						positionSpan-=0.8;

					var posSpanMvt = 0;
					posSpanMvt = (sommeCumul + precPos) / 2;
					posSpanMvt = (100*posSpanMvt) / somme;
					posSpanMvt -=2;

					precPos = sommeCumul;

					$('div.center').append("<img class='barre' title='"+$('#mov_'+i).val()+"' style='left:"+position+"% ' src='./includes/images/barre_mvt.png'>");

					$('div.center').append('<span class="spanMvt" style="left:'+posSpanMvt+'%">'+i+'</span>');

					if (tabTime["pausemov_"+i] != undefined){
						sommeCumul+= parseInt(tabTime["pausemov_"+i]);
						position = (100*sommeCumul)/somme;

						positionSpan = position - 1;

						if(sommeCumul >= 100)
							positionSpan-=0.8;

						precPos = sommeCumul;

						$('div.center').append("<img class='barre' style='left:"+position+"% ' src='./includes/images/barre.png'> <span class='spanTime' style='left:"+positionSpan+"%'>"+sommeCumul+"</span>");
					}
				}
				
			};
		}

		//create move
		nb_ss_mov = 1
		function add_one_ss_mov(){
			nb_ss_mov = nb_ss_mov+1;
			$('#add_ss_mov').append('<tr><td><div><label for="nom_mov">sous-mouvement '+nb_ss_mov+'</label></div><div class="tab_nom"><fieldset class="form-group"><input type="text" title="Nom du sous mouvement composant le mouvement." class="input_shadow form-control" id="ss_mov_'+nb_ss_mov+'" placeholder="nom du mouvement" /></fieldset></div><div class="tab_vit"><fieldset class="form-group"><input type="text" title="Vitesse de lecture du sous mouvement, comprise entre 1 et 10. Une vitesse 9 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible" class="input_shadow form-control" id="speed_'+nb_ss_mov+'" placeholder="vitesse" /></fieldset></div><div class="tab_pause"><fieldset class="form-group"><input type="text" title="Décalage temporel entre le début du mouvement et le début du sous mouvement. L\'unité est l\'incrément (environ 0.25s en vitesse normale, cette valeur augmente si la vitesse diminue). Plus l\'offset est grand, et plus le mouvement démarrera avec du retard." class="input_shadow form-control" id="offset_'+nb_ss_mov+'" placeholder="offset" /></fieldset></div><!--td class="pull-right"><fieldset class="form-group"><button class="btn btn-danger supp_ligne" title="Supprimer la ligne"><span class="glyphicon glyphicon-trash"></span></button></fieldset></td--></td></tr>');
			$('#ss_mov_'+nb_ss_mov).autocomplete({
				source: moveTags
			});
		};
		//create exo
		nb_mov = 1
		function add_one_mov(){
			nb_mov = nb_mov+1;
			$('#add_mov').append('<tr><tr><td colspan="3"><div><label for="type_exo">mouvement '+nb_mov+'</label></div><div class="tab_nom"><fieldset class="form-group"><input type="text" title="Nom du mouvement composant l\'exercice à créer." class="input_shadow form-control mvt_timeline" id="mov_'+nb_mov+'" placeholder="nom du mouvement" /></fieldset></div><div class="tab_vit"><fieldset class="form-group"><input type="text" title="Vitesse de lecture du mouvement, comprise entre 1 et 10. Une vitesse 5 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible" class="input_shadow form-control" id="speedmov_'+nb_mov+'" placeholder="vitesse" /></fieldset></div><div class="tab_pause"><fieldset class="form-group"><input type="text" title="Correspond à la pause après le mouvement concerné. La pause est en secondes." class="input_shadow form-control pause_timeline" id="pausemov_'+nb_mov+'" placeholder="pause" /></fieldset></div></td><!--td class="pull-right"><fieldset class="form-group"><button title="Supprimer la ligne" class="btn btn-danger supp_ligne"><span class="glyphicon glyphicon-trash" ></span></button></fieldset></td--><tr><td id="add_voice_'+nb_mov+'" colspan="3"></td></tr><tr><td><div class="tab_voix_vide"> </div><div class="tab_voix_button"><button type="button" class="btn btn-info" onclick="add_one_voice(\''+nb_mov+'\')">Voix</button></div></td></tr></tr></tr></tr>');
			$('#mov_'+nb_mov).autocomplete({
				source: moveTags
			});
		};
		//create seance
		nb_exo = 1
		function add_one_exo(){
			nb_exo = nb_exo+1;
			$('#add_exo').append('<tr><td colspan="3"><div><label for="type_exo">exercice '+nb_exo+'</label></div><div class="tab_nom"><fieldset class="form-group"><input type="text" title="Nom de l exercice composant le fichier à créer." class="input_shadow form-control" id="exo_'+nb_exo+'" placeholder="nom de l exercice" /></fieldset></div><div class="tab_vit"><fieldset class="form-group"><input type="text" title="Vitesse de lecture de l exercice, comprise entre 1 et 10. Une vitesse 5 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible" class="input_shadow form-control" id="speedexo_'+nb_exo+'" placeholder="vitesse" /></fieldset></div><div class="tab_pause"><fieldset class="form-group"><input type="text" title="Correspond à la pause après l exercice concerné. La pause est en secondes." class="input_shadow form-control" id="pauseexo_'+nb_exo+'" placeholder="pause" /></fieldset></div></td><!--td class="pull-right"><fieldset class="form-group"><button title="Supprimer la ligne" class="btn btn-danger supp_ligne"><span class="glyphicon glyphicon-trash" ></span></button></fieldset></td--></tr>');
			$('#exo_'+nb_exo).autocomplete({
				source: exoTags
			});
		};
		//add voice create exo
		nb_voice = 0
		function add_one_voice(moveId){
			nb_voice = nb_voice+1;
			$('#add_voice_'+moveId).append('<div class="tab_voix_vide">Voix '+nb_voice+'</div><div class="tab_voix_time"><fieldset class="form-group"><input type="text" title="Temps correspondant au début du commentaire oral." class="form-control voice_time" id="voice_time_'+nb_voice+'" placeholder="temps" /></fieldset></div><div class="tab_voix_com"><fieldset class="form-group"><input type="text" title="Texte du commentaire oral que dira le robot." class="form-control voice_texte" id="voice_texte_'+nb_voice+'" placeholder="commentaire oral" /></fieldset></div> <div class="tab_voix_test"><input type="button" class="btn btn-info" id="btn-test-tts" onclick="testTTS($(\'#voice_texte_'+nb_voice+'\').val());"/></div>');
		};
	</script>

	<script src="JS/functions.js"></script>
	<audio id="audioPlayer">
		<source src="includes/sons/done.ogg">
	</audio>
	<audio id="audioPlayerWarning">
		<source src="includes/sons/warning.ogg">
	</audio>
	<audio id="audioPlayerAlert">
		<source src="includes/sons/alert.ogg">
	</audio>

<?php include "includes/footer.php"; ?>	
