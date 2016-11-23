var dataListe = [];
var jsondataBDD = "";
var nb_tempsBDD = 0;
var activeMove = "";
var partComp = false;
var init = false;
var poppyName = "192.168.0.125";//"poppygr.local";	//nom du robot poppy ou adresse IP
var uptodate = true;
var seuilTemp = 55;				//seuil d'alerte de surchauffe moteur
var player = "";				// son lors fin d'enregistrement mouvement
var playerWarning = "";			// son lors surchauffe robot (warning avant mode securite)
var playerAlert = "";			// son lors de l'activation mode securite du robot (surchauffe)

function majPoppyName(){
	poppyName = $('#poppyName').val();
	console.log("poppyName : "+poppyName)
	GetIP()
	ReceiveMovelist()
}

function Compliant() {
	//var compliant= $('#compliant').val();
	var compliant= $('#compliant').prop('checked');
	if(partComp == false){  //toggle les boutons seulement si partComp=false : bouton ON/OFF ttes les parties
		partComp=true;
		if(compliant==false){
			//arrete tout (AU)
			StopExo()
			$('#compliantT').bootstrapToggle("off");
			$('#compliantBG').bootstrapToggle("off");
			$('#compliantBD').bootstrapToggle("off");
			$('#compliantCol').bootstrapToggle("off");
			$('#compliantJD').bootstrapToggle("off");
			$('#compliantJG').bootstrapToggle("off");
			$.ajax({
				url: 'http://'+poppyName+':4567/?Submit=set+robot+compliant&poppyParts=',
				type:'POST',
				statusCode: {
					200: function() {
						console.log("Poppy is compliant" );
					},
					0:function(data){		//error, not connected
						console.log('error : Poppy is not connected');
						document.getElementById('poppyConnected').src="includes/images/notconnected.png";
					}
				}
			});
		} else{
			$('#compliantT').bootstrapToggle("on");
			$('#compliantJD').bootstrapToggle("on");
			$('#compliantJG').bootstrapToggle("on");
			$('#compliantCol').bootstrapToggle("on");
			$('#compliantBD').bootstrapToggle("on");
			$('#compliantBG').bootstrapToggle("on");
			$.ajax({
				url: 'http://'+poppyName+':4567/?Submit=set+robot+non-compliant&poppyParts=',
				type:'POST',
				statusCode: {
					200: function() {
						console.log("Poppy is not compliant" );
						initSound();						
					},
					0:function(data){		//error, not connected
						console.log('error : Poppy is not connected');
						document.getElementById('poppyConnected').src="includes/images/notconnected.png";
					}
				}
			});
		}
	}
	partComp=false;
}

function PartNonCompliant(poppyParts="") {
	var nbParts = 0;
	var semiPoppyParts = [];
	var nbsemiNbParts = 0;
	
	if(partComp==false){
		partComp = true;
		var poppyParts = [];
		if($('#compliantT').prop('checked')){
			poppyParts.push("tete");
			nbParts = nbParts+1;
		}
		if($('#compliantBG').prop('checked')){
			poppyParts.push("bras_gauche");
			nbParts = nbParts+1;
		}
		if($('#compliantBD').prop('checked')){
			poppyParts.push("bras_droit");
			nbParts = nbParts+1;
		}
		if($('#compliantCol').prop('checked')){
			poppyParts.push("colonne");
			nbParts = nbParts+1;
		}
		if($('#compliantJG').prop('checked')){
			poppyParts.push("jambe_gauche");
			nbParts = nbParts+1;
		}
		if($('#compliantJD').prop('checked')){
			poppyParts.push("jambe_droite");
			nbParts = nbParts+1;
		}
		
		$('input:checked[name=poppyPartsMou]').each(function(i,o){
			if($.inArray($(o).val(), poppyParts) > -1){
				semiPoppyParts.push($(o).val());
				nbsemiNbParts = nbsemiNbParts + 1;
			}
		});
        //MAJ bouton ON/OFF de Poppy entier
		if(nbParts==0){
			partComp=false;
			$('#compliant').bootstrapToggle("off");
		}
		else{
			$('#compliant').bootstrapToggle("on"); //MAJ de l'affichage bouton ON/OFF seulement
			$.ajax({
				url: 'http://'+poppyName+':4567/?Submit=set+robot+non-compliant&poppyParts='+poppyParts,
				type:'POST',
				statusCode: {
					200: function() {
						console.log("Poppy is not compliant" );
						$('input:checkbox[name=poppyParts]').removeAttr('checked');
						$('#modal_part_non_compliant').modal('hide');
						initSound();
					},
					0:function(data){		//error, not connected
						console.log('error : Poppy is not connected');
						document.getElementById('poppyConnected').src="includes/images/notconnected.png";
					}
				}
			});
		}
	}
	if(nbsemiNbParts!=0){
		semiCompliant(semiPoppyParts);
	}
}

function semiCompliant(semiPoppyParts="") {
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=set+robot+semi-compliant&poppyParts='+semiPoppyParts,
		type:'POST',
		statusCode: {
			200: function() {
				console.log("Poppy is semi-compliant" );
				initSound();
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
}

function SaveInitPos() {
	var posName = prompt('Please enter the name of the initial position','debout');
        if (posName == null || posName == "") {
		alert('canceled');
		return;
	}
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=save+init+pos&posName='+posName,
		type:'POST',
		statusCode: {
			201: function(data) {
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	})
}

function GoInitPos(pos = "undefined") {
	initSound();
	$('#exoConfig').hide();
	if(pos == "undefined"){
		var posName = prompt('Please enter the name of the initial position','debout');
		if (posName == null || posName == "") {
			alert('canceled');
			return;
		}
	}
	else{
		var posName = pos;
	}
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=go+init+pos&posName='+posName,
		type:'POST',
		statusCode: {
			201: function(data) {
				console.log(data);
				partComp=true;
				$('#compliantT').bootstrapToggle("on");
				$('#compliantBG').bootstrapToggle("on");
				$('#compliantBD').bootstrapToggle("on");
				$('#compliantCol').bootstrapToggle("on");
				$('#compliantJG').bootstrapToggle("on");
				$('#compliantJD').bootstrapToggle("on");
				$('#compliant').bootstrapToggle("on");
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	})
}

function GoDebout(){
	GoInitPos(pos="debout");
}

function GoAssis(){
	GoInitPos(pos="assis");
}

function stopPlayer(playerName){
	if (playerName=="player"){
		player.pause();
	}
	if (playerName=="playerWarning"){
		playerWarning.pause();
	}
	if (playerName=="playerAlert"){
		playerAlert.pause();
	}
}

function SaveSsMovePart() {
	$('#exoConfig').hide();
	var moveName = $('#nom_mvt_ss_part').val();
	var playedMove = $('#nom_playedMove').val();
	var poppyParts = [];
	var semiMou = ''

	$('input:checked[name=poppyPartsCreatePart]').each(function(i,o){
		poppyParts.push($(o).val());
	});
	
	$('input:checked[name=semiMou]').each(function(i,o){
		semiMou = $(o).val();
	});
	
	if (moveName == null || moveName == "") {
		alert('Veuillez entrer un nom pour ce mouvement');
		return;
	}
	moveName = moveName.replace(/\350|\351|\352|\353/g,"e");	//Ë, È, Í, Î
	moveName = moveName.replace(/\340|\341|\342|\343|\344|\345|\346/g,"a");
	moveName = moveName.replace(/\354|\355|\356|\357/g,"i");
	moveName = moveName.replace(/\371|\372|\373|\374/g,"u");
	moveName = moveName.replace(/\360|\362|\363|\364|\365|\366/g,"o");
	moveName = moveName.replace(/\347/g,"c");	// Á
	if (playedMove == null ) {
		alert('annulÈ');
		return;
	}

	if (poppyParts == null || poppyParts.length == 0) {
		poppyParts.push('tete');
		alert('error, poppyParts set to tete');
	}
	player.currentTime = 0;
	player.play();
	player.pause();
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=save+part+move&moveName='+moveName+'&poppyParts='+poppyParts+'&semiMou='+semiMou+'&playedMove='+playedMove,
		type:'POST',
		statusCode: {
			201: function() {
				console.log("move saved in Poppy." );
				player.play();			//joue un son
				setTimeout('stopPlayer("player")', 2200);
				//Si le mouvement a bien √©t√© sauvegard√©, on l'enregistre dans la bdd
				//Oblig√© de faire avec un post car on est dans du js !
				$.post("./core/functions/moves.php?action=insert", {"moveName" : moveName, "moveType" : "mov", "parts" : poppyParts}).done(function(data){
					console.log(data);
				});
				insertJsonBDD(moveName);
				$('#nom_mvt_ss_part').val('');
				$('input:checkbox[name=poppyPartsCreatePart]').removeAttr('checked');
				$('#modal_create_ss_mvt_part').modal('hide');
				
				ReceiveMovelist();
			},
			200:function(data){
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
}

function Symetry(moveName="") {
	var listeFiles = []
	if (moveName==""){
		var moveName = prompt('Please enter the name of the move part','move_part_name');
		if (moveName == null || moveName == "") {
			alert('canceled');
			return;
		}
	}
	listeFiles.push(moveName)
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=symetry&moveName='+moveName,
		type:'POST',
		statusCode: {
			201: function(data) {
				console.log("symetry file "+moveName+"Sym created");
				$.post("./core/functions/moves.php?action=insertMov" , {"listeFiles" : listeFiles, "moveType" : data, "moveName" : moveName+"Sym"}).done(function(data){
					console.log(data);
				});
				insertJsonBDD(moveName+"Sym");
				$.post("./core/functions/moves.php?action=symetry" , {"moveName" : moveName+"Sym"}).done(function(data){
					console.log(data);
				});
				ReceiveMovelist();
			},
			200:function(data){
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
}

function Reverse(moveName="") {
	var listeFiles = []
	if (moveName == ""){
		var moveName = prompt('Please enter the name of the move part','moveName');
		if (moveName == null || moveName == "") {
			alert('canceled');
			return;
		}
	}
	listeFiles.push(moveName)
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=reverse&moveName='+moveName,
		type:'POST',
		statusCode: {
			201: function(data) {
				console.log("reverse file "+moveName+"Rev created");
				$.post("./core/functions/moves.php?action=insertMov" , {"listeFiles" : listeFiles, "moveType" : data, "moveName" : moveName+"Rev"}).done(function(data){
					console.log(data);
				});
				insertJsonBDD(moveName+"Rev");
				ReceiveMovelist();
			},
			200:function(data){
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
}

function CreateMove(previsu = "False") {
	var moveConfig ;
	var listeFiles = [];
	var moveName = $('#nom_mov').val();
	if (moveName== "") {
		alert('enter a name');
		return
	}
	moveName = moveName.replace(/\350|\351|\352|\353/g,"e");	//Ë, È, Í, Î
	moveName = moveName.replace(/\340|\341|\342|\343|\344|\345|\346/g,"a");
	moveName = moveName.replace(/\354|\355|\356|\357/g,"i");
	moveName = moveName.replace(/\371|\372|\373|\374/g,"u");
	moveName = moveName.replace(/\360|\362|\363|\364|\365|\366/g,"o");
	moveName = moveName.replace(/\347/g,"c");	// Á
	var type = 'mov';
	moveConfig = '{"type":"'+type+'"';
	var nb_fichiers=0;
	var vide = 0;
	for (var iter = 1; iter < nb_ss_mov+1; iter++){
		var namefile = $('#ss_mov_'+iter).val();
		if (namefile != "") {
			var offset = $('#offset_'+iter).val();
			if (!(offset>=0) || offset == "") {
				offset = 0;
			}
			var speed = $('#speed_'+iter).val();
			if (!(speed>=1 && speed<=10) || speed == "") {
				speed= 9;
				//alert('error, speed set to 9 (must be [1-10])');
			}
			moveConfig = moveConfig+',"fichier'+(iter-vide)+'":{"namefile":"'+namefile+'"';
			moveConfig = moveConfig+',"offset":'+offset
			moveConfig = moveConfig+',"speed":'+speed+'}';
			nb_fichiers = nb_fichiers + 1;
			listeFiles.push(namefile);
		}
		else{
			vide = vide +1;
		}
	}
	moveConfig = moveConfig+', "nb_fichiers":'+nb_fichiers+'}';
	if(nb_fichiers == 0){
		alert("error: no file")
		return
	}
	$.ajax({
	  url: 'http://'+poppyName+':4567/?Submit=create+move&moveName='+moveName+'&previsu='+previsu,
	  type:'POST',
	  data:  moveConfig,
	  statusCode: {
		201: function(data) {
			console.log(data);
			if(previsu=="False"){
				$('#nom_mov').val('');
				$('#type_mov').val('');
				$('#modal_create_mov').modal('hide');
				nb_ss_mov = 1;
				$('#add_ss_mov').html('<tr><td><fieldset class="form-group"><input type="text" class="form-control" id="ss_mov_'+nb_ss_mov+'" placeholder="ss_mov_name" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="speed_'+nb_ss_mov+'" placeholder="speed [1-10] (normal=9)" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="offset_'+nb_ss_mov+'" placeholder="offset" /></fieldset></td></tr>');
			
				$.post("./core/functions/moves.php?action=insertMov" , {"listeFiles" : listeFiles, "moveType" : type, "moveName" : moveName}).done(function(data){
					console.log(data);
				});
				insertJsonBDD(moveName);
			ReceiveMovelist();
			}	
		},
		200:function(data){
			console.log(data);
		},
		0:function(data){		//error, not connected
			console.log('error : Poppy is not connected');
			document.getElementById('poppyConnected').src="includes/images/notconnected.png";
		}
	   }
	});
}

function PrevisualisationMove(){
	CreateMove(previsu = "True");
}

function CreateExo() {
	var exoConfig ;
	var listeFiles = [];
	var exoName = $('#nom_exo').val();
	if (exoName== "") {
		alert('enter a name');
		return;
	}
	exoName = exoName.replace(/\350|\351|\352|\353/g,"e");	//Ë, È, Í, Î
	exoName = exoName.replace(/\340|\341|\342|\343|\344|\345|\346/g,"a");
	exoName = exoName.replace(/\354|\355|\356|\357/g,"i");
	exoName = exoName.replace(/\371|\372|\373|\374/g,"u");
	exoName = exoName.replace(/\360|\362|\363|\364|\365|\366/g,"o");
	exoName = exoName.replace(/\347/g,"c");	// Á
	var type = $('#type_exo').val();
	if (!(type == 'exo' || type == 'seance')){
		alert('error, choose type : exo or seance');
		return;
	}
	exoConfig = '{"type":"'+type+'"';
	var nb_fichiers=0;
	var vide = 0;
	for (var iter = 1; iter < nb_mov+1; iter++){
		var namefile = $('#mov_'+iter).val();
		if (namefile != "") {
			exoConfig = exoConfig+',"fichier'+(iter-vide)+'":{"namefile":"'+namefile+'"';
			var vitesse = $('#speedexo_'+iter).val();
			if (!(vitesse>=1 && vitesse<=10) || vitesse == "") {
				vitesse= 5;
				//alert('warning, vitesse set to 5 (must be [1-10])');
			}
			exoConfig = exoConfig+',"vitesse":'+vitesse;
			var pause= $('#pause_'+iter).val();
			if (!(pause>=0 && pause<50) || pause == "") {
				pause = 5;
				//alert('warning, pause set to 5 (must be [0-49])');
			}
			exoConfig = exoConfig+',"pause":'+pause+'}';
			nb_fichiers = nb_fichiers + 1;
			listeFiles.push(namefile);
		}
		else{
			vide = vide +1;
		}
	}
	exoConfig = exoConfig+', "nb_fichiers":'+nb_fichiers+'}';
	if(nb_fichiers == 0){
		alert("error: no file")
		return
	}
	$.ajax({
	  url: 'http://'+poppyName+':4567/?Submit=create+exo&exoName='+exoName,
	  type:'POST',
	  data:  exoConfig,
	  statusCode: {
			201: function(data) {
				console.log(data);
				$('#nom_exo').val('');
				$('#type_exo').val('');
				$('#modal_create_exo').modal('hide');
				nb_mov = 1;
				$('#add_mov').html('<tr><td><fieldset class="form-group"><input type="text" class="form-control" id="mov_'+nb_mov+'" placeholder="mov_name" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="speedexo_'+nb_mov+'" placeholder="vitesse [1-10] (normal=5)" /></fieldset></td><td><fieldset class="form-group"><input type="text" class="form-control" id="pause_'+nb_mov+'" placeholder="pause" /></fieldset></td></tr>');
			
				$.post("./core/functions/moves.php?action=insertMov" , {"listeFiles" : listeFiles, "moveType" : type, "moveName" : exoName}).done(function(data){
					console.log(data);
				});
				insertJsonBDD(exoName);
				ReceiveMovelist();
			},
			200:function(data){
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});	
}

function GoMove(rev = "False") {    //non utilis√© pour l'instant ! y a la fonction Go plus bas
	$('#exoConfig').hide();
	var moveName = $('#nom_mvt').val();
	var speed = $('#speed').val();
	var poppyParts = [];

	$('input:checked[name=poppyPartsGo]').each(function(i,o){
		poppyParts.push($(o).val());
	});

	if (moveName == null || moveName == "") {
		alert('Veuillez entrer un nom pour ce mouvement');
		return;
	}
	
        if (speed !=1 && speed!=2 && speed!=3 && speed!=4) {
		//alert('error, speed set to 2')
		speed = 2;
	}
	if(rev == "False"){
		var submit = "go+move";
	}
	else{
		var submit = "go+reverse";
	}
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit='+submit+'&moveName='+moveName+'&speed='+speed+'&poppyParts='+poppyParts,
		type:'POST',
		statusCode: {
			201: function(data) {
				console.log(data);
				partComp=true;
				$('#compliant').bootstrapToggle("on");
				$('input:checkbox[name=poppyPartsGo]').removeAttr('checked');
				$('#modal_go_move').modal('hide');
			},
			200:function(data){
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	})
}

function GoRev() {
	GoMove(rev = "True");
}

var fin_exo = 0;

function verifFinExo(){
	if(fin_exo == 1){
		$('#exoConfig').hide();   //A mettre en commentaire si on veut garder le visuel apres la seance
		$('#progressbar').progressbar('value', 100);
		$("#progressbarlabel").html("Termin√© !");
		document.getElementById('Go'+activeMove).className = "play";
		activeMove = "";
		return;
	}
	var exo= document.getElementById('Go'+activeMove).className;
	if(exo!="resume"){
		$.ajax({
			url: 'http://'+poppyName+':4567/?Submit=verif+fin+exo',
			type:'POST',
			dataType : 'json',
			statusCode: {
				201: function(data) {
					
					console.log(jsondata);
					$('#Go').val('start');
					
					fin_exo = 1
				},
				200: function(data){

					jsondata=data.responseText.replace("u'","\"");
					while(jsondata.search("u'")!=-1){
						jsondata=jsondata.replace("u'","\"");
					}
					while(jsondata.search("'")!=-1){
						jsondata=jsondata.replace("'","\"");
					}
					
					jsondata = JSON.parse(jsondata);
					
					console.log(jsondata);
					
					//On met tout en noir
					$('.exo').css('background-color','white');
					
					//On met dans une certaine couleur l'exo et le mouvement en cours
					if(jsondata["num_exo"] == 0){
						$('#mvt_'+jsondata["num_mov"]).css('background-color', 'rgba(0, 172, 193, 0.43)');
					} else{
						$('#exo_'+jsondata["num_exo"]).css('background-color', 'rgba(0, 172, 193, 0.43)');
						$('#exo_'+jsondata["num_exo"]+'_'+jsondata["num_mov"]).css('background-color', 'rgba(0, 172, 193, 0.43)');
					}
					
					//On modifie la barre de progression
					var info = jsondata["info"].split(" ");
					var total = (info[1].split("/"))[1];
					var en_cours = (info[1].split("/"))[0];
					
					$('#progressbar').progressbar('value', en_cours/total * 100);
					$("#progressbarlabel").html(Math.round(en_cours/total*100)+" %");
				},
				0:function(data){		//error, not connected
					console.log('error : Poppy is not connected');
					document.getElementById('poppyConnected').src="includes/images/notconnected.png";
				}
			}
		});
	}
	setTimeout("verifFinExo()", 3000);
}

var fin_mov = 0;

function verifFinMov(){
	if(fin_mov == 1){
		document.getElementById('Go'+activeMove).className = "play";
		activeMove = "";
		return;
	}
	var mov= document.getElementById('Go'+activeMove).className;
	if(mov!="resume"){
		$.ajax({
			url: 'http://'+poppyName+':4567/?Submit=verif+fin+mov',
			type:'POST',
			dataType : 'json',
			statusCode: {
				201: function(data) {
					$('#Go').val('start');
					
					fin_mov = 1;
				},
				200: function(data){
					//do nothing
				},
				0:function(data){		//error, not connected
					console.log('error : Poppy is not connected');
					document.getElementById('poppyConnected').src="includes/images/notconnected.png";
				}
			}
		});
	}
	setTimeout("verifFinMov()", 1000);
}

function clickFleche(){
	if ($(this).hasClass('active')){
		  $(this).next().slideToggle();		          
		  $(this).children().html('‚ñ∏');    
		  $(this).removeClass('active');
	} else {
		$(this).next().slideToggle();	
		$(this).children().html('‚ñæ');
		$(this).addClass('active');
	}  	
}


function Go(exoName) {
	initSound();
	var exo= document.getElementById('Go'+exoName).className;
	if(exo=="play"){
		StopExo();
		$.ajax({
			url: 'http://'+poppyName+':4567/?Submit=go&exoName='+exoName,
			type:'POST',
			dataType:'json',
			statusCode: {
				202: function(data) {		//mouvement
					console.log(data.responseText);
					partComp=true;
					$('#compliant').bootstrapToggle("on");
					if(document.getElementById('parts'+exoName).innerHTML.includes("T")){
						partComp=true;
						$('#compliantT').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("BrasG")){
						partComp=true;
						$('#compliantBG').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("BrasD")){
						partComp=true;
						$('#compliantBD').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("Col")){
						partComp=true;
						$('#compliantCol').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("JambeG")){
						partComp=true;
						$('#compliantJG').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("JambeD")){
						partComp=true;
						$('#compliantJD').bootstrapToggle("on");
                        partComp=false;
					}
					document.getElementById('Go'+exoName).className = "pause";
					activeMove = exoName;
					fin_mov=0;
					verifFinMov();          //A DECOMMENTER ! pour detecter fin mov. 
				},
				201: function(data) {		//exo ou seance
					jsondata=data.responseText.replace("u'","\"");
					while(jsondata.search("u'")!=-1){
						jsondata=jsondata.replace("u'","\"");
					}
					while(jsondata.search("'")!=-1){
						jsondata=jsondata.replace("'","\"");
					}
					jsondata=$.parseJSON(jsondata)
					console.log(jsondata);
					
					$('#exoConfig').show();
					$('#progressbar').progressbar('value', 0);
					$("#progressbarlabel").html("0 %");
					$("#progressbarlabel").nextAll().remove();
					
					$('#exoConfig').append('<div id="nom_seance">' + exoName + '</div>' );
					for (i=1; i<=jsondata['nb_fichiers']; i++){
						if (jsondata[i]['nb_fichiers'] >0){
							$('#exoConfig').append('<div class="exo nom_exo active" id="exo_'+i+'"> <span class="flecheDeroul">‚ñæ</span> ' + jsondata[i]['nom']+'</div>');
							var texte = "";
							texte+= '<div class="containerMvts">';
							for (j=1; j<=jsondata[i]['nb_fichiers']; j++){
								texte+='<div class="exo nom_mvt" id="exo_'+i+'_'+j+'">' + jsondata[i][j]+'</div>';
							}
							texte+='</div>';
							$('#exoConfig').append(texte);	
						}
						else{
							$('#exoConfig').append('<div class="exo nom_mvt" id="mvt_'+i+'">' + jsondata[i]+"</div>");
						}
					}
					$('.nom_exo').on ('click', clickFleche);
					
					partComp=true;
					$('#compliant').bootstrapToggle("on");
					if(document.getElementById('parts'+exoName).innerHTML.includes("T")){
						partComp=true;
						$('#compliantT').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("BrasG")){
						partComp=true;
						$('#compliantBG').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("BrasD")){
						partComp=true;
						$('#compliantBD').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("Col")){
						partComp=true;
						$('#compliantCol').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("JambeG")){
						partComp=true;
						$('#compliantJG').bootstrapToggle("on");
                        partComp=false;
					}
					if(document.getElementById('parts'+exoName).innerHTML.includes("JambeD")){
						partComp=true;
						$('#compliantJD').bootstrapToggle("on");
                        partComp=false;
					}
					document.getElementById('Go'+exoName).className = "pause";
					fin_exo=0;
					activeMove = exoName;
					verifFinExo();
				},
				200:function(data){
					console.log(data.responseText);
				},
				0:function(data){		//error, not connected
					console.log('error : Poppy is not connected');
					document.getElementById('poppyConnected').src="includes/images/notconnected.png";
				}
			}
		})
	} 
	else if (exo=='pause'){
		$.ajax({
			url: 'http://'+poppyName+':4567/?Submit=pause+exo',
			type:'POST',
			statusCode: {
				201: function(data) {
					console.log(data);
					document.getElementById('Go'+exoName).className = "resume";	
				},
				200:function(data){
					console.log(data);
				},
				0:function(data){		//error, not connected
					console.log('error : Poppy is not connected');
					document.getElementById('poppyConnected').src="includes/images/notconnected.png";
				}
			}
		})
	}
	else if (exo=='resume'){
		$.ajax({
			url: 'http://'+poppyName+':4567/?Submit=resume+exo',
			type:'POST',
			statusCode: {
				201: function(data) {
					console.log(data);
					document.getElementById('Go'+exoName).className = "pause";	
				},
				200:function(data){
					console.log(data);
				},
				0:function(data){		//error, not connected
					console.log('error : Poppy is not connected');
					document.getElementById('poppyConnected').src="includes/images/notconnected.png";
				}
			}
		})
	}
	partComp=false;
}
	
	


function StopExo(moveName = "") {
	
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=stop+exo',
		type:'POST',
		statusCode: {
			201: function(data) {
				console.log(data);
				fin_exo = 1;
			},
			200: function(data){
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
    $('#exoConfig').hide();
	if (moveName != ""){
		if (document.getElementById('Go'+moveName).className != "play" || activeMove != ""){ 
			document.getElementById('Go'+moveName).className = "play";
		}
	}
	if (activeMove != ""){
		document.getElementById('Go'+activeMove).className = "play";
		activeMove = "";
	}
		
}

function RemoveMove(moveName="") {
	if (moveName==""){
		var moveName = prompt('Please enter the name of the move part','move_part_name');
		if (moveName == null || moveName == "") {
			alert('canceled');
			return;
		}
	}
	var confirm = prompt('Are you sure you want to delete '+moveName+' ?', 'yes');
	if (confirm != 'yes'){
		return;
	}
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=remove+move&moveName='+moveName,
		type:'POST',
		statusCode: {
			201: function(data) {
				console.log(data);
				ReceiveMovelist();
				RemoveFileDatabase(moveName);
			},
			200:function(data){
				console.log(data);
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
}

function RemoveFileDatabase(moveName="") {
	if (moveName == ""){
		var moveName = prompt('Please enter the name of the move part','move_part_name');
		if (moveName == null || moveName == "") {
			alert('canceled');
			return;
		}
	}
	$.post("./core/functions/moves.php?action=deleteMov", {"moveName" : moveName}).done(function(data){
		console.log(data);
		AfficheMovelist();
	});
}

function majBdD(){
	setTimeout("ReceiveMovelist()", 1000);
	majBdDsuite();
}

function majBdDsuite(){
	$.post('./core/functions/moves.php?action=majBdD', {"listeMov" : dataListe}).done(function(data){
		console.log(data);
		$.post('./core/functions/moves.php?action=checkJson').done(function(data){
			//console.log(data);
			data = JSON.parse(data);
			for (var key in data){
				console.log(data[key]["moveName"]);
				ReceiveFile(data[key]["moveName"], BDD="true");
			}
		});
	});
}

function majPoppy(){
	$.post('./core/functions/moves.php?action=getMovelist').done(function(database){
		data = JSON.parse(database);
		console.log(data);
		for (var key in data){
			moveName = data[key]["moveName"];
			if (data[key]["id_moveType"]=="1"){
				var type = "mov";
			}else if (data[key]["id_moveType"]=="2"){
				var type = "exo";
			}else if (data[key]["id_moveType"]=="3"){
				var type = "seance";
			}
			var poppyParts = [];
			if (data[key]["tete"]==1){
				poppyParts.push("tete");
			} 
			if (data[key]["bras_gauche"]==1){
				poppyParts.push("bras_gauche");
			} 
			if (data[key]["bras_droit"]==1){
				poppyParts.push("bras_droit");
			} 
			if (data[key]["colonne"]==1){
				poppyParts.push("colonne");
			} 
			if (data[key]["jambe_gauche"]==1){
				poppyParts.push("jambe_gauche");
			} 
			if (data[key]["jambe_droite"]==1){
				poppyParts.push("jambe_droite");
			}
			dataToSend = data[key]["jsondata"];
			dataToSend = JSON.parse(dataToSend);
			dataToSend["poppyParts"]=poppyParts;
			dataToSend = JSON.stringify(dataToSend)
			$.ajax({
				url: 'http://'+poppyName+':4567/?Submit=add+move&moveName='+moveName+'&type='+type,
				type:'POST',
				data: dataToSend,
				statusCode: {
					201: function(data){
						//console.log("added");
					},
					200:function(data){
						//console.log("already exists");
					},
					0:function(data){		//error, not connected
						console.log('error : Poppy is not connected');
						document.getElementById('poppyConnected').src="includes/images/notconnected.png";
					}
				}
			});
		}
		ReceiveMovelist();
	});
}

function SendFile() {
	var dataToSend ;
	var namefile = prompt('Please enter the name of file','currentPos.json');
        if (namefile == null || namefile == "") {
		alert('canceled');
		return;
	}
	jsonfile='JS/'+namefile;
	$.getJSON(jsonfile, function(donnees) {
		dataToSend=JSON.stringify(donnees);
	}).done(function(){
		$.ajax({
			url: 'http://'+poppyName+':4567/?Submit=senddata&jsonfile='+namefile,
			type:'POST',
			data:  dataToSend,
			//dataType: 'json',
			error: function(jqXHR, textStatus, errorThrown) {
		        console.log('error : Poppy is not connected');
			    //console.log(jqXHR,textStatus, errorThrown);
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
	        }
		}).success( function(data){
			console.log(data);
		});
	});
}

function ScanResults() {
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=getMesure',
		type:'GET',
		dataType: 'json',
		statusCode: {
			200: function(data) {
				results = data
				temperatureMax = Math.max(results["temperature"]["max"])
				//console.log("temperature maximale : "+temperatureMax)
				$('#temperatureMax').html(temperatureMax);
				if (temperatureMax>=seuilTemp){
					if($('#temperatureMax').css('color')!='rgb(255, 0, 0)'){
						alert("Attention ! Poppy surchauffe !");
					} 
					$('#temperatureMax').css('color','rgb(255,0,0)');
				}
				else{
					$('#temperatureMax').css('color','rgb(255,255,223)');
				}
				var playWarning = false;
				var playAlert = false;
				for (var key in data['poppyPart_alert']){
					if (data['poppyPart_alert'][key]=='warning'){
						if ($('#compliantPart'+key).css('color') == 'rgb(255, 255, 255)'){
							playWarning = true;
						}
						$('#compliantPart'+key).css('color','rgb(255,100,30)');
						$('#compliantPart'+key).css('font-weight','bold');
					}
					else if (data['poppyPart_alert'][key]=='stop'){
						if ($('#compliantPart'+key).css('color') != 'rgb(255, 30, 30)'){
							playAlert = true;
						}
						$('#compliantPart'+key).css('color','rgb(255,30,30)');
						$('#compliantPart'+key).css('font-weight','bold');
					}
					else if (data['poppyPart_alert'][key]=='ok'){
						$('#compliantPart'+key).css('color','rgb(255,255,255)');
						$('#compliantPart'+key).css('font-weight','');
					}
				}
				if(playAlert==true){
					playerAlert.currentTime=0;
					playerAlert.play();
					setTimeout('stopPlayer("playerAlert")', 2200);
				}
				else if(playWarning==true){
					playerWarning.currentTime=0;
					playerWarning.play();
					setTimeout('stopPlayer("playerWarning")', 2200);
				}
				$('#poppyName').val(poppyName);
				if (data['compliant']=="u'True'"){
					partComp=true;
					$('#compliant').bootstrapToggle("off");
				}
				else{
					partComp=true;
					$('#compliant').bootstrapToggle('on');
				}
				if (data['compliantT']=="u'True'"){
					partComp=true;
					$('#compliantT').bootstrapToggle("off");
				}
				else{
					partComp=true;
					$('#compliantT').bootstrapToggle('on');
				}
				if (data['compliantBG']=="u'True'"){
					partComp=true;
					$('#compliantBG').bootstrapToggle("off");
				}
				else{
					partComp=true;
					$('#compliantBG').bootstrapToggle('on');
				}
				if (data['compliantBD']=="u'True'"){
					partComp=true;
					$('#compliantBD').bootstrapToggle("off");
				}
				else{
					partComp=true;
					$('#compliantBD').bootstrapToggle('on');
				}
				if (data['compliantCol']=="u'True'"){
					partComp=true;
					$('#compliantCol').bootstrapToggle("off");
				}
				else{
					partComp=true;
					$('#compliantCol').bootstrapToggle('on');
				}
				if (data['compliantJD']=="u'True'"){
					partComp=true;
					$('#compliantJD').bootstrapToggle("off");
				}
				else{
					partComp=true;
					$('#compliantJD').bootstrapToggle('on');
				}
				if (data['compliantJG']=="u'True'"){
					partComp=true;
					$('#compliantJG').bootstrapToggle("off");
				}
				else{
					partComp=true;
					$('#compliantJG').bootstrapToggle('on');
				}
				partComp=false;
				if (uptodate==true){
					document.getElementById('poppyConnected').src="includes/images/connected.png";
				}
				else{
					document.getElementById('poppyConnected').src="includes/images/notUptodate.png";
				}
			},
			0:function(data){		//error, not connected
				//console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
	setTimeout("ScanResults()", 5000);
}

function CheckIfPoppyUptodate(nb_mov, nb_exo, nb_seance){
	$.post("./core/functions/moves.php?action=getMovesNumber").done(function(data){
		var movNumber=data[0];
		var exoNumber=data[1];
		var seanceNumber=data[2];
		if(nb_mov!=movNumber || nb_exo!=exoNumber || nb_seance!=seanceNumber){
			console.log("Poppy n'est pas a jour");
			uptodate=false;
			document.getElementById('poppyConnected').src="includes/images/notUptodate.png";
		}
		else{
			console.log("Poppy est a jour");
			uptodate=true;
		}
	});
}

function ReceiveFile(namefile = 'nothg', BDD = "false") {
	var jsondata="" ;
	if (namefile == 'nothg') {
		var namefile = prompt('Please enter the name of file','movelist');
		if (namefile === null || namefile == ''){
			alert('canceled');
			return;
		}
	}
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=receivedata&jsonfile='+namefile+'&BDD='+BDD,
		type:'GET',
		dataType: 'json',
		statusCode: {
			201: function(data) {
				jsondata = data
				console.log(jsondata) 
				if (namefile == 'movelist'){
					dataListe = jsondata;		// maj variable globale
					if (jsondata['compliant']=="u'True'"){
						partComp=true;
						$('#compliant').bootstrapToggle("off");
					}
					else{
						partComp=true;
						$('#compliant').bootstrapToggle('on');
					}
					if (jsondata['compliantT']=="u'True'"){
						partComp=true;
						$('#compliantT').bootstrapToggle("off");
					}
					else{
						partComp=true;
						$('#compliantT').bootstrapToggle('on');
					}
					if (jsondata['compliantBG']=="u'True'"){
						partComp=true;
						$('#compliantBG').bootstrapToggle("off");
					}
					else{
						partComp=true;
						$('#compliantBG').bootstrapToggle('on');
					}
					if (jsondata['compliantBD']=="u'True'"){
						partComp=true;
						$('#compliantBD').bootstrapToggle("off");
					}
					else{
						partComp=true;
						$('#compliantBD').bootstrapToggle('on');
					}
					if (jsondata['compliantCol']=="u'True'"){
						partComp=true;
						$('#compliantCol').bootstrapToggle("off");
					}
					else{
						partComp=true;
						$('#compliantCol').bootstrapToggle('on');
					}
					if (jsondata['compliantJD']=="u'True'"){
						partComp=true;
						$('#compliantJD').bootstrapToggle("off");
					}
					else{
						partComp=true;
						$('#compliantJD').bootstrapToggle('on');
					}
					if (jsondata['compliantJG']=="u'True'"){
						partComp=true;
						$('#compliantJG').bootstrapToggle("off");
					}
					else{
						partComp=true;
						$('#compliantJG').bootstrapToggle('on');
					}
					partComp=false;
					CheckIfPoppyUptodate(jsondata['nb_mov'], jsondata['nb_exo'],jsondata['nb_seance']);
				}
				else if (BDD == "true"){
					jsondataBDD = jsondata;
					nb_tempsBDD = jsondata["nb_temps"];
					$.post('./core/functions/moves.php?action=insertJson', {"moveName" : namefile, "jsondata" : jsondataBDD, "nb_temps" : nb_tempsBDD}).done(function(data){
						console.log(data);
						AfficheMovelist();
					});
				}
				if (uptodate==true){
					document.getElementById('poppyConnected').src="includes/images/connected.png";
				}
				else{
					document.getElementById('poppyConnected').src="includes/images/notUptodate.png";
				}
			},
			200:function(data){
				console.log("does not exist");
			},
			0:function(data){		//error, not connected
				console.log('error : Poppy is not connected');
				document.getElementById('poppyConnected').src="includes/images/notconnected.png";
			}
		}
	});
	if(init == false){
		init = true;
		setTimeout("WaitBeforeScan()", 5000);
	}
}

function insertJsonBDD(moveName){
	ReceiveFile(moveName, BDD = "true");
}

function ReceiveMovelist() {
	ReceiveFile('movelist');
}

function AfficheMovelist(playerOnly = "false"){
	var data;
	$.post('./core/functions/moves.php?action=getMovelist').done(function(database){
		data = JSON.parse(database);
		console.log(data);
		
		$('#majBdD').nextAll().remove();
		$('#tableMoves_wrapper').remove();
		$('#movelist').append('<table id="tableMoves" class="table table-striped table-bordered">'+
								'<thead>'+
									'<tr>'+
										'<th>Nom du mouvement</th>'+
										'<th>Type</th>'+
										'<th>Parties utilis√©es</th>'+
										'<th>Actions</th>'+
										'<th>Player</th>'+
									'</tr>'+
								'</thead>'+
								
								'<tbody>'+
								'</tbody>'+
							'</table>');
		
		var texte = "";
		
		for (var key in data){
			texte += "<tr>";
			texte += "<td>"+data[key]["moveName"]+"</td>";
			moveName = data[key]["moveName"];
			
			if (data[key]["id_moveType"]=="1"){
				var type = "mouvement";
			}else if (data[key]["id_moveType"]=="2"){
				var type = "exercice";
			}else if (data[key]["id_moveType"]=="3"){
				var type = "seance";
			}
			texte += "<td>"+type+"</td>";
			
			var poppyParts = "";
			if (data[key]["tete"]=="1"){
				poppyParts += "T ";
			}
			if (data[key]["colonne"]=="1"){
				poppyParts += "Col ";
			}
			if (data[key]["bras_gauche"]=="1"){
				poppyParts += "BrasG ";
			}
			if (data[key]["bras_droit"]=="1"){
				poppyParts += "BrasD ";
			}
			if (data[key]["jambe_gauche"]=="1"){
				poppyParts += "JambeG ";
			}
			if (data[key]["jambe_droite"]=="1"){
				poppyParts += "JambeD ";
			}
			texte += "<td id='parts"+moveName+"'>"+poppyParts+"</td>";
			
			texte += "<td><input type='button' title='symetry' onclick='Symetry(&quot;"+moveName+"&quot;)' id='symetry' /><input type='button' title='Reverse' onclick='Reverse(&quot;"+moveName+"&quot;)' id='reverse'/> <input type='button' title='delete' onclick='RemoveMove(&quot;"+moveName+"&quot;)' id='delete'/></td>";
			texte += "<td><input type='button' title='play' onclick='Go(&quot;"+moveName+"&quot;)' id='Go"+moveName+"' class='play' style='color:#00ba00'/> <input type='button' title='stop' onclick='StopExo(&quot;"+moveName+"&quot;)' id='stop"+moveName+"' class='stop' style='color:#ea0000'/> </td>";
			texte += "</tr>";
			
		}
				
		$('#tableMoves tbody').append(texte);	
		$('#tableMoves').DataTable( {
			language: {		
				processing:     "Traitement en cours...",
				search:         "Rechercher&nbsp;:",
				lengthMenu:    "Afficher _MENU_ &eacute;l&eacute;ments",
				info:           "Affichage de l'&eacute;lement _START_ &agrave; _END_ sur _TOTAL_ &eacute;l&eacute;ments",
				infoEmpty:      "Affichage de l'&eacute;lement 0 &agrave; 0 sur 0 &eacute;l&eacute;ments",
				infoFiltered:   "(filtr&eacute; de _MAX_ &eacute;l&eacute;ments au total)",
				infoPostFix:    "",
				loadingRecords: "Chargement en cours...",
				zeroRecords:    "Aucun &eacute;l&eacute;ment &agrave; afficher",
				emptyTable:     "Aucune donn√©e disponible dans le tableau",
				paginate: {
					first:      "Premier",
					previous:   "Pr&eacute;c&eacute;dent",
					next:       "Suivant",
					last:       "Dernier"
				},
				aria: {
					sortAscending:  ": activer pour trier la colonne par ordre croissant",
					sortDescending: ": activer pour trier la colonne par ordre d√©croissant"
				}
			}
		} );
	});
}

function GetIP() {
	$.ajax({
		url: 'http://'+poppyName+':4567/?Submit=getIP',
		type:'GET',
		dataType: 'text',
		statusCode: {
			200: function(data) {
				poppyIP = data
				console.log("adresse IP du robot : "+poppyIP)	
			},
		}
	});
}

function WaitBeforeScan(){
	setTimeout("ScanResults()", 5000);
}

function loadSound() {
	player = document.querySelector('#audioPlayer');
	playerWarning = document.querySelector('#audioPlayerWarning');
	playerAlert = document.querySelector('#audioPlayerAlert');
}

function initSound(){
	playerWarning.play();
	playerWarning.pause();
	playerAlert.play();
	playerAlert.pause();
}

function initPage() {
	loadSound();
	$('#poppyName').val(poppyName);
	StopExo();
	ReceiveMovelist();
	AfficheMovelist();
	GetIP();
}