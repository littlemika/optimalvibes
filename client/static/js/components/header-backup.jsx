import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';
import SearchSong from './search-song.jsx';
import SpotifyPlaylist from './spotify-playlist.jsx';
import YoutubePlaylist from './youtube-playlist.jsx';
import SearchBar from './search-bar.jsx'



// http://stackoverflow.com/questions/35224113/react-change-class-name-on-state-change
var DEFAULT_OPTION_INDEX = 0;
var MENU_OPTIONS = [
	{
		key: 0,
		path: '/', 
		name: "Search",
		iconType: "image",
		iconName: "search.png",
		iconNameGrey: "search_grey.png",
		description: "Download Single Song"
	},
	{ 
		key: 1,
		path: '/spotify', 
		name: "Spotify",
		iconType: "image",
		iconName: "spotify.png",
		iconNameGrey: "spotify_grey.png",
		description: "Download Spotify Playlist"
	},
	{ 
		key: 2,
		path: '/youtube', 
		name: "Youtube",
		iconType: "image",
		iconName: "youtube.png" ,
		iconNameGrey: "youtube_grey.png",
		description: "Download Youtube Playlist"
	}
];


/*
	Use:

	this.props{
		glyphicon : glyphicon,
		name : name,
		description : description
	}
		
*/

class Option extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			activeIndex : 0
		}


		//alert(this.props.selected_option);
	}

	toggleMenuOptions(){
		this.props.onClick(this.props.index);
	}

	
	render () {
		return (

			<div className="option center-content-h" onClick={this.toggleMenuOptions.bind(this)}>
				<div className="inner">
					<div className="left">
						{ this.props.isActive ? <img src={"/public/images/icons/" +  this.props.iconName} height="50" alt={this.props.name + " icon"}/> : 
												<img src={"/public/images/icons/" +  this.props.iconNameGrey} height="50" alt={this.props.name + " icon"}/>}
					</div>
					<div className="right">			
						<ul className="info">
							<li className={this.props.isActive ? "selected-option name":"unselected-option name"}>{this.props.name}</li>
							<li className="desc">{this.props.description}</li>
						</ul>
					
					</div>
				</div>
			</div>
			
			
		);
	}


}

// $(document).ready(function(){

// });
$(window).scroll(function () {

 	var body_scroll_top = $('#body').scrollTop();	
 	console.log(body_scroll_top);

 	// if(body_scroll_top == 0) {
 	// 	$('#header').animate({
		//     top: "+=400"
		// }, 700, function() {
		//     $(this).css({"position":"static", "z-index":"1"});
		// });

		// $('#body').animate({
		//     top: "+=400"
		// }, 700, function() {
		//     $(this).css("top","-100px");
		// });

 	// }

 
});



export default class Header extends React.Component {


	constructor(props) {
		super(props);
		

		this.state = {
			activeIndex : DEFAULT_OPTION_INDEX
		};

		this.toggleMenuOptions = this.toggleMenuOptions.bind(this);
		this.search = this.search.bind(this);

	}


	toggleMenuOptions (index) {
		this.setState({
			activeIndex : index
		});
	}	

	
	search(i,event) {
		event.preventDefault();
		var url = this.refs.search_in.value;

		var header_element = document.getElementById('header');

		var header_height = header_element.offsetHeight;
		var fixed_header_height = 50;			// when the page scrolls down we want to transition into a fixed header
		var scroll_page = header_height - fixed_header_height;


		$('#header').animate({
		    top: "-=400"
		}, 700, function() {
		    $(this).css({"position":"fixed", "z-index":"1"});
		});

		$('#body').animate({
		    top: "-=400"
		}, 700, function() {
		    $(this).css("top","100px");
		});

		document.getElementById('upper-header').style.display = 'hidden';
		document.getElementById('middle-header').style.height = 'hidden';


		//header_element.style.top = '-' + fixed_header_height.toString() + 'px';
		//
		//header_element.style.position = 'fixed';

		$.ajax({
			url: '/music/search',
			dataType: 'json',
			data: {'url' : url, 'artist' : 'artist', 'song' : 'songname'},
			method: 'POST',
			success: function(data){
				
				// request failed
				if(data['status']['success'] == false) {
				//	alert(data['status']['description']);
				} else {
					//alert(data['status']['success']);
					//success do stuff
				}
			
			},
			error: function(request, status, error){
				// alert(status);
				// alert(error);
				// alert(response);
				// alert(request.responseText);
			}
		});
	}


	render() {
	
		return (
			<Router>
			<header id="header">
				<div className="outer" id="outer-header">
				
					{/* START container-fluid  */}
					<div className="container-fluid" id="container-header">	
					
						{/* START row upper */}
						<div className="row upper" id="upper-header">
							<div className="col-sm-12">
								<span className="site-name">Optimal<span className="small">Vibes</span></span>
							</div>
							<br/><br/><br/><br/><br/>
						</div>
						{/* END row upper */}
						{/* START row middle */}
						<div className="row middle" id="middle-header">
							<div className="col-sm-offset-2 col-sm-8">
								<div className="row">
									{
										MENU_OPTIONS.map(dict => {
											return (
												<div className="col-sm-4"  key={dict['name']}>
													<Link className="link-override" to={dict['path']}>
														<Option className="option-link" glyphicon="glyphicon-search"
															key = {dict['key']}
															index= {dict['key']}
															iconType= {dict['iconType']} 
															iconName={dict['iconName']} 
															iconNameGrey={dict['iconNameGrey']}
															name={dict['name']} 
															description={dict['description']} 
															isActive={this.state.activeIndex === dict['key']}
															onClick={this.toggleMenuOptions.bind(dict['key'])}
														/>
													</Link>
												</div>
											)
										})

									}
	
								</div>

								<br/><br/><br/>
								{/* START search bar */}
								<div className="row">
									<div className="col-xs-3 col-sm-3">
										<span className="label pull-right ">Youtube URL</span>
									</div>
									<div className="col-xs-6 col-sm-6">
										<div className="form-group search-bar-size">
											<input type="text" className="form-control" ref="search_in" id="search_in" placeholder={ this.props.placeholder }/>
										</div>
									</div>
									<div className="col-xs-3 col-sm-3">
										<div className="form-group search-bar-size">
											<button onClick={this.search.bind(this)} className="submit btn btn-default btn-success">
												Search
											</button>
											{/*<button type="submit" className="btn btn-default btn-success">{ this.props.submit_text }</button>*/}
										</div>
									</div>
								</div>
								{/* END search bar */}
							</div>
						</div>
						{/* END row middle */}
						{/* START row bottom */}
						<br/>
						<div className="row bottom" id="bottom-header">
							<Route exact path="/" component={SearchSong}/>
							<Route path="/spotify" component={SpotifyPlaylist}/>
							<Route path="/youtube" component={YoutubePlaylist}/>							
						</div>
						{/* END row bottom */}
					</div>
					{/* END container-fluid  */}	
	
				{/* END outer  */}
				</div>

			</header>
			</Router>

		);
	}
}

