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
			</div>
			<br>
			<div class="power">
				<div>
					<span class="title2">Alimentation</span>  
					<input id='compliant' data-toggle="toggle" data-onstyle="warning" type="checkbox" data-size="mini" data-height="15">
				</div>

				<br>
				
				<div> 
					<span class="title3">Position initiale</span>  
					<!--input type="button" value="debout" onclick='GoDebout()' id='goDebout' /--> 
					<input type="button" value="chaise" onclick='GoChaise()' id='goChaise' /> 
					<!--input type="button" value="assis" onclick='GoAssis()' id='goAssis' /--><br> <br>
				</div>

				<div style="display:flex"> 
					<span class="title3 mauto">Volume Poppy</span>  
					<input type="range" min="0" max="1" step="0.05" class="slide" id="rangeVolume" value="0.5"/>
					<input type="text" style="width:40px" class="mauto" value="0.5" id="inputVolume"/>
					<input type="submit" value="OK" class="mauto" onclick="setRobotVolume()" />
				</div>

				<br />

				<div style="display:flex"> 
					<span class="title3 mauto">Seuil Kinect</span>  
					<input type="range" min="0" max="300" step="10" class="slide" id="rangeKinect" value="150"/>
					<input type="text" style="width:40px" class="mauto" value="150" id="inputKinect"/>
					<input type="submit" value="OK" class="mauto" onclick="setThresholdKinect()" />
					<br>
				</div>

			</div>

			<!--suivi avancement exercice/seance en cours-->
			<div id='exoConfig'>
				<div id="progressbar"></div>
				<div id="progressbarlabel"></div>
			</div>
			
			<div class="poppyimage">
				<input type="button" value="créer une seance" id='createSeance' data-toggle="modal" data-target="#modal_create_seance" style="width:100%; margin-top:10px"/> 
			</div>
			<!--input type="button" value="save init pos" onclick='SaveInitPos()' id='saveinitpos' /><br> <br--> 
			<!--input type="button" value="receive movefile" onclick="ReceiveFile()" id='Datareceive'/> <br> <br-->
		</div>

	</div>
	<div id=contenu> </div>
</div>
	<!-- Modal -->
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
							<select class="nom_exo_kine" id="exo_1" title="Nom de l'exercice composant le fichier à créer.">
								<option value="">aucun exercice</option>
								<option value="etirementLaterauxKine">etirements Lateraux</option>
								<option value="etirementLaterauxBTendu">etirements Lateraux bras tendu</option>
								<option value="rotationTroncKine">rotation tronc</option>
								<option value="cacheTeteKine">respiration</option>
							</select>
						</fieldset></div>
						<div class="tab_vit" style="display:none"><fieldset class="form-group">
							<input type="text" title="Vitesse de lecture de l'exercice, comprise entre 1 et 10. Une vitesse 5 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible." class="input_shadow form-control" id="speedexo_1" placeholder="vitesse" />
						</fieldset></div>
						<div class="tab_repet"><fieldset class="form-group">
							<input type="text" title="Nombre de répétitions de l'exercice par le sujet." class="input_shadow form-control" id="nb_repet_1" placeholder="répétitions" />
						</fieldset></div>
						<div class="tab_pause"><fieldset class="form-group">
							<input type="text" title="Correspond à la pause après l'exercice concerné et entre les répétitions. La pause est en secondes." class="input_shadow form-control" id="pauseexo_1" placeholder="pause" />
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

	<script>
		var tabTime = [];
		
		$(function(){
			
			var progressbar = $( "#progressbar" );
	 
			progressbar.progressbar({
				value: 0
			});

		    $('#compliant').change(function() {
		    	
		    	Compliant();
		    });

			$(document).on('click', '.supp_ligne', function(){
				$(this).closest("tr").remove();
			});
		});

		//create seance
		nb_exo = 1
		function add_one_exo(){
			nb_exo = nb_exo+1;
			$('#add_exo').append('<tr><td colspan="3"><div><label for="type_exo">exercice '+nb_exo+'</label></div><div class="tab_nom"><fieldset class="form-group"><select class="nom_exo_kine" id="exo_'+nb_exo+'" title="Nom de l\'exercice composant le fichier à créer."><option value="">aucun exercice</option><option value="etirementLaterauxKine">etirements Lateraux</option><option value="etirementLaterauxBTendu">etirements Lateraux bras tendu</option><option value="rotationTroncKine">rotation tronc</option><option value="cacheTeteKine">respiration</option></select></fieldset></div><div class="tab_vit" style="display:none"><fieldset class="form-group"><input type="text" title="Vitesse de lecture de l exercice, comprise entre 1 et 10. Une vitesse 5 correspond à la vitesse normale. Plus la valeur est faible et plus la vitesse sera faible." class="input_shadow form-control" id="speedexo_'+nb_exo+'" placeholder="vitesse" /></fieldset></div><div class="tab_repet"><fieldset class="form-group"><input type="text" title="Nombre de répétitions de l\'exercice par le sujet." class="input_shadow form-control" id="nb_repet_'+nb_exo+'" placeholder="répétitions" /></fieldset></div><div class="tab_pause"><fieldset class="form-group"><input type="text" title="Correspond à la pause après l exercice concerné et entre les répétitions. La pause est en secondes." class="input_shadow form-control" id="pauseexo_'+nb_exo+'" placeholder="pause" /></fieldset></div></td><!--td class="pull-right"><fieldset class="form-group"><button title="Supprimer la ligne" class="btn btn-danger supp_ligne"><span class="glyphicon glyphicon-trash" ></span></button></fieldset></td--></tr>');
		};

		$('#rangeVolume').on('input', function(){
			$(this).next().val($(this).val());
		});

		$('#rangeKinect').on('input', function(){
			$(this).next().val($(this).val());
		});
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
