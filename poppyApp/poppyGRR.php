<?php 
session_start();
//error_reporting(0);
require 'core/database/connect.php';
$errors = array();
include 'core/functions/moves.php';
//include 'includes/overall/overallheader.php'; 
include "includes/head.php";
include "includes/header.php";
?>
<div id="container">
<body onload="initPage()">
<!--partie exercice/seance en cours-->
	<div id='exoConfig'>
		<div id="progressbar"></div>
		<div id="progressbarlabel"></div>
	</div>

<!--partie boutons-->
	<div id='application'>
		<section id="movelist">
		</section>
		<!-- TODO !!!!!!!!!! -->
		<section id="boutons">
			<section id="poppy">
				<img src="includes/images/notconnected.png" id="poppyConnected">
				Poppy : 
				<txt id="poppyName"></txt>
				<txt id="tempMax">Tmax : <txt id="temperatureMax"></txt></txt> 
			</section>
			<br>
			<section class="power">
			<section id="title">Alimentation</section>
			<table id="compliantTable"> 
			<tr id="firstLine">
				<td text style="font-weight:bold;" id="compliantPart">Tous les moteurs </td>
				<td><input id='compliant' data-toggle="toggle" data-onstyle="warning"type="checkbox" data-size="mini" data-height="15"></td>
				<td id="semiMou">semi-mou</td>
			</tr>
			<tr id="compliantRow">
				<td id="compliantPart">Tete</td>
				<td><input id='compliantT' data-toggle="toggle" data-onstyle="warning"type="checkbox" data-size="mini"> </td>
				<td id="semiMou"><input type="checkbox" name="poppyPartsMou" value="tete" ></td>
			</tr>
			<tr id="compliantRow">
				<td id="compliantPart">BrasG</td> 
				<td><input id='compliantBG' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini"> </td>
				<td id="semiMou"><input type="checkbox" name="poppyPartsMou" value="bras_gauche"></td>
			</tr>
			<tr id="compliantRow">
				<td id="compliantPart">BrasD</td>
				<td><input id='compliantBD' data-toggle="toggle" data-onstyle="warning"type="checkbox" data-size="mini"> </td>
				<td id="semiMou"><input type="checkbox" name="poppyPartsMou" value="bras_droit" ></td>
			</tr>
			<tr id="compliantRow">
				<td id="compliantPart">Colonne </td>
				<td><input id='compliantCol' data-toggle="toggle" data-onstyle="warning"type="checkbox" data-size="mini"> </td>
				<td id="semiMou"><input type="checkbox" name="poppyPartsMou" value="colonne"></td>
			</tr>
			<tr id="compliantRow">
				<td id="compliantPart">JambeG </td>
				<td><input id='compliantJG' data-toggle="toggle" data-onstyle="warning"type="checkbox" data-size="mini"> </td>
				<td id="semiMou"><input type="checkbox" name="poppyPartsMou" value="jambe_gauche"></td>
			</tr>
			<tr id="compliantRow">
				<td id="compliantPart">JambeD </td>
				<td><input id='compliantJD' data-toggle="toggle" data-onstyle="warning"type="checkbox" data-size="mini"> </td>
				<td id="semiMou"><input type="checkbox" name="poppyPartsMou" value="jambe_droite"></td>
			</tr>
			<!--tr id="compliantRow">
				<td></td>
				<td></td>
				<td><input type="button" value="rafraichir" id='semicompliant' onclick='semiCompliant()'/></td>
			</tr-->
			</table>
			<!--input type="button" value="switch ON" onclick='Compliant()' id='compliant'  /-->  
			 
			<br><section> <text id="title" style="font-size:16px;">Position initiale :</text> &nbsp 
				<input type="button" value="debout" onclick='GoDebout()' id='goDebout' /> 
				<input type="button" value="assis" onclick='GoAssis()' id='goAssis' /><br> 
				</section>
			</section>
			<section class="poppyimage">
			<center> <img src="includes/images/poppyImage.png" id="poppyImage" ></center> 
			</section>
			<section class="save">
			<section id="title">Enregistrement</section>
			<input type="button" value="enregistrer mouvement" id='SavSsMovePart' data-toggle="modal" data-target="#modal_create_ss_mvt_part" /> <br>
			<input type="button" value="creer mouvement" id='createMove' data-toggle="modal" data-target="#modal_create_mov" /> <br>
			<input type="button" value="creer exercice" id='createExo' data-toggle="modal" data-target="#modal_create_exo"/> <br>
			</section>
			<!--input type="button" value="save init pos" onclick='SaveInitPos()' id='saveinitpos' /><br> <br--> 
			<!--input type="button" value="receive movefile" onclick="ReceiveFile()" id='Datareceive'/> <br> <br-->
		</section>
	</div>
	<div id="contenu">
		<input type="button" value="Mettre à jour la base" id="majBdD" onclick="majBdD()" /><br> <br>
	</div>

	<script>
	  $(function() {
	    $('#compliant').change(function() {
	      Compliant();
	    })
	  })
	  //TODO !!!!!!!!!
	  $(function() {
	    $('#compliantT').change(function() {
	      PartNonCompliant();
	    })
	  })
	  $(function() {
	    $('#compliantBG').change(function() {
	      PartNonCompliant();
	    })
	  })
	  $(function() {
	    $('#compliantBD').change(function() {
	      PartNonCompliant();
	    })
	  })
	  $(function() {
	    $('#compliantCol').change(function() {
	      PartNonCompliant();
	    })
	  })
	  $(function() {
	    $('#compliantJG').change(function() {
	      PartNonCompliant();
	    })
	  })
	  $(function() {
	    $('#compliantJD').change(function() {
	      PartNonCompliant();
	    })
	  })
	  //END TODO
	</script>

	<!-- Modal -->
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
					<label for="nom_mvt_ss_part">Nom du mouvement</label> <input type="text" class="form-control" id="nom_mvt_ss_part" placeholder="nom_part_mouv" />
				</fieldset>
				<fieldset class="form-group">
					<label for="nom_playedMove">Nom du mouvement joué pendant la sauvegarde</label> <input type="text" class="form-control" id="nom_playedMove" placeholder="" />
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
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Création d'un mouvement</h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<label for="nom_mov">Nom du mouvement</label> <input type="text" class="form-control" id="nom_mov" placeholder="nom_move" />
				</fieldset>
			</div>
			<!--partie dynamique pour ajouter un nombre n de ss_mov(_part) dans la fusion-->
			<table id="add_ss_mov">
				<tr>
					<td><fieldset class="form-group">
						<input type="text" class="form-control" id="ss_mov_1" placeholder="ss_mov_name" />
					</fieldset></td>
					<td><fieldset class="form-group">
						<input type="text" class="form-control" id="speed_1" placeholder="speed [1-10] (normal=9)" />
					</fieldset></td>
					<td><fieldset class="form-group">
						<input type="text" class="form-control" id="offset_1" placeholder="offset" />
					</fieldset></td>
				</tr>
			</table>
			<button type="button" class="btn btn-info" onclick="add_one_ss_mov()">Add</button>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-default" onclick="PrevisualisationMove()">Prévisualiser</button>
			  <button type="button" class="btn btn-info" onclick="CreateMove()">Sauvegarder</button>
			</div>
		  </div>
		</div>
	</div>
	
	<div class="modal fade" id="modal_create_exo" role="dialog">
		<div class="modal-dialog">
		  <!-- Modal content-->
		  <div class="modal-content">
			<div class="modal-header">
			  <button type="button" class="close" data-dismiss="modal">&times;</button>
			  <h4 class="modal-title">Création d'un exercice</h4>
			</div>
			<div class="modal-body">
				<fieldset class="form-group">
					<label for="nom_exo">Nom du fichier</label> <input type="text" class="form-control" id="nom_exo" placeholder="nom_exo" />
				</fieldset>
				<fieldset class="form-group">
					<label for="type_exo">type du fichier (exo/seance)</label> <input type="text" class="form-control" id="type_exo" placeholder="" />
				</fieldset>
			</div>
			<!--partie dynamique pour ajouter un nombre n de move dans la concatenation-->
			<table id="add_mov">
				<tr>
					<td><fieldset class="form-group">
						<input type="text" class="form-control" id="mov_1" placeholder="mov_name" />
					</fieldset></td>
					<td><fieldset class="form-group">
						<input type="text" class="form-control" id="speedexo_1" placeholder="vitesse [1-10] (normal=5)" />
					</fieldset></td>
					<td><fieldset class="form-group">
						<input type="text" class="form-control" id="pause_1" placeholder="pause" />
					</fieldset></td>
				</tr>
			</table>
			<button type="button" class="btn btn-info" onclick="add_one_mov()">Add</button>
			<div class="modal-footer">
			  <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
			  <button type="button" class="btn btn-info" onclick="CreateExo()">Sauvegarder</button>
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
		$(function(){
			
			var progressbar = $( "#progressbar" );
	 
			progressbar.progressbar({
				value: 0
			});
		});
		//create move
		nb_ss_mov = 1
		function add_one_ss_mov(){
			nb_ss_mov = nb_ss_mov+1;
			$('#add_ss_mov').append('<tr><td><fieldset class="form-group"><input type="text" class="form-control" id="ss_mov_'+nb_ss_mov+'" placeholder="ss_mov_name" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="speed_'+nb_ss_mov+'" placeholder="speed [1-10] (normal=9)" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="offset_'+nb_ss_mov+'" placeholder="offset" /></fieldset></td></tr>');
		};
		//create exo
		nb_mov = 1
		function add_one_mov(){
			nb_mov = nb_mov+1;
			$('#add_mov').append('<tr><td><fieldset class="form-group"><input type="text" class="form-control" id="mov_'+nb_mov+'" placeholder="mov_name" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="speedexo_'+nb_mov+'" placeholder="vitesse [1-10] (normal=5)" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="pause_'+nb_mov+'" placeholder="pause" /></fieldset></td></tr>');
		};
	</script>

	<script src="JS/functions.js"></script>
</body>

<?php include "includes/footer.php"; ?>	
