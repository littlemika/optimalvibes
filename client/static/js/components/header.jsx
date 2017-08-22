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

// spotify:user:1212962782:playlist:0dnfOzFamuV4VvRFgJqUeD
// https://www.youtube.com/playlist?list=PLXPKEW_UjQXVxozm3O_AG1pEncuANxqxM
// https://www.youtube.com/watch?v=5dmQ3QWpy1Q
var DEFAULT_OPTION_INDEX = 0;
var MENU_OPTIONS = [
	{
		key: 0,
		path: '/', 
		name: "Search",
		iconType: "image",
		iconName: "search.png",
		iconNameGrey: "search_grey.png",
		description: "Download Single Song",
		searchTxt: "Search",
		validation: "https://www.youtube.com/watch?v=",
		lngDesc: '		\
										\
			<p className="popover-content"> \
				Type in either <span className="highlight">(artist & song name)</span> or <span className="highlight">(youtube URL)</span> \
			</p> \
		'	
	},
	{ 
		key: 1,
		path: '/spotify', 
		name: "Spotify",
		iconType: "image",
		iconName: "spotify.png",
		iconNameGrey: "spotify_grey.png",
		description: "Download Spotify Playlist",
		searchTxt: "Spotify URI",
		validation: "spotify:user:",
		lngDesc: '	\
			<p className="popover-content"> \
				<span>Copy and paste the spotify uri into the search input.</span> \
				<ol>	\
					<li>Right click a playlist in spotify</li>	\
					<li>Select <i>Copy Spotify URI</i></li> \
				</ol>	\
				<br/>	\
				<b>Example: </b>	\
				<i>spotify:user:1212962782:playlist:0dnfOzFamuV4VvRFgJqUeD</i>	\
			</p>	\
			\
		'
	},
	{ 
		key: 2,
		path: '/youtube', 
		name: "Youtube",
		iconType: "image",
		iconName: "youtube.png" ,
		iconNameGrey: "youtube_grey.png",
		description: "Download Youtube Playlist",
		searchTxt: "Youtube Playlist URL",
		validation: "https://www.youtube.com/playlist?list=",
		lngDesc: '	\
			<p className="popover-content">	\
				<span>Copy and paste the link to a youtube playlist url into the search form.</span>	\
				<ol>	\
					<li>Go to youtube.com</li>	\
					<li>Login if needed</li>	\
					<li>On the menu bar located to the left of the screen look under <i>Library</i> select and open a playlist</li>	\
					<li>Copy the link in the toolbar located at the top of the screen</li>	\
				</ol>	\
				<br/>	\
				<b>Example:</b><br/>	\
				<i>https://www.youtube.com/playlist?list=PLXPKEW_UjQXVxozm3O_AG1pEncuANxqxM</i> 	\
			</p>	\
			\
		'
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

			<div className="option center-content-h" onClick={this.toggleMenuOptions.bind(this)}  data-html="true" data-content={this.props.lngDesc} rel="popover" data-placement="bottom" >
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


var shrinkHeader = 300;

$(document).ready(function() {
	$('.option').popover({ trigger: "hover" });


	$(window).scroll(function() {
	    var scroll = getCurrentScroll();
	    if ( scroll >= shrinkHeader ) {
	        $('.header').addClass('shrink');
	        $('#tracks').css('margin-top','400px');
        }
	    else {
	        $('.header').removeClass('shrink');
	        $('#tracks').css('margin-top','60px');
	    }
	
	});
	///women/dresses_and_jumosuits, yellow, small
	function getCurrentScroll() {
  	  return window.pageYOffset || document.documentElement.scrollTop;
    }

 
 

});



export default class Header extends React.Component {


	constructor(props) {
		super(props);
		

		this.state = {
			activeIndex : DEFAULT_OPTION_INDEX,
			searchText : 'Search',
			searchErrMsg : '',
			grabTrackURL : ''
		};

		this.toggleMenuOptions = this.toggleMenuOptions.bind(this);
		this.search = this.search.bind(this);

	}

	toggleMenuOptions (searchTxt, index) {
		this.setState({
			activeIndex : index,
			searchText : searchTxt
		});
	}	

	
	search(i,event) {
		event.preventDefault();
		var search_val = this.refs.search_in.value;


		// search input validation
		for(i=0; i<MENU_OPTIONS.length; i++)
		{

			var option = MENU_OPTIONS[i]
			
			// not selected option
			if(option['key'] != this.state.activeIndex) 
				continue

			if (!search_val.includes(option['validation'])) {
				this.setState({ searchErrMsg : 'Not valid format! Input must contain: ' + option['validation'] });
				return;

			} else {

				this.setState({	searchErrMsg : '' });
				var option_type = option['name'].toLowerCase();

				// if spotify uri then the user must first authenticate
				if (option_type == 'spotify')
				{

					// get auth url
					$.ajax({
						url: '/spotify/authorize',
						dataType: 'json',
						data: {'spotify_uri':search_val},
						method: 'GET',
						success: function(data){
							
							// success
							var spotify_auth_url = data['spotify_auth_url'];
							window.open(spotify_auth_url, '_self');
							
							
						},
						error:  function(request, status, error){
							alert(error);
							alert(status)
						}
					})
					
					return;
					
				} else {
					var self = this;

					$('#loading').css('visibility','visible');

					// otherwise, just download track to server
					$.ajax({
						url: '/download',
						contentType: 'application/json',
						data: JSON.stringify({
							url: search_val,
							download_type: option_type
						}),
						dataType: 'json',
						method: 'POST',
						success: function(data) {
							alert(data['grab_track_url']);
							alert(data['status']);
							
							self.setState({
								grabTrackURL: data['grab_track_url']
							});

							$('#loading').css('visibility','hidden');
						},
						error: function(request, status, error){
							alert(error);
							alert(status);
						}
					});
				}

				break;
			}
			
		}	

		window.scrollBy(0,shrinkHeader);


		// $.ajax({
		// 	url: '/music/search',
		// 	dataType: 'json',
		// 	data: {'url' : search_val, 'artist' : 'artist', 'song' : 'songname', 'option_type': option_type},
		// 	method: 'POST',
		// 	success: function(data){
				
		// 		// request failed
		// 		if(data['status']['success'] == false) {
		// 		//	alert(data['status']['description']);
		// 		} else {
		// 			//alert(data['status']['success']);
		// 			//success do stuff
		// 		}
			
		// 	},
		// 	error: function(request, status, error){
		// 		// alert(status);
		// 		// alert(error);
		// 		// alert(response);
		// 		// alert(request.responseText);
		// 	}
		// });

	}


	render() {
	
		return (
			<Router>
				<div className="header">
					<div className="container">
						{/* START row upper */}	
						<div className="row upper">
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
												<div className="col-sm-4 option-holder"  key={dict['name']}>
													<Link className="link-override" to={dict['path']}>
														<Option className="option-link" glyphicon="glyphicon-search"
															key = {dict['key']}
															index= {dict['key']}
															iconType= {dict['iconType']} 
															iconName={dict['iconName']} 
															iconNameGrey={dict['iconNameGrey']}
															name={dict['name']} 
															description={dict['description']} 
															lngDesc={dict['lngDesc']}
															isActive={this.state.activeIndex === dict['key']}
															onClick={this.toggleMenuOptions.bind(dict['key'], dict['searchTxt'])}
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
										<span className="label pull-right ">{this.state.searchText}</span>
									</div>
									<div className="col-xs-6 col-sm-6">
										<div className="form-group search-bar-size">
											<input defaultValue="spotify:user:1212962782:playlist:5pG6xbQwHuKo0CbP1EJowx" type="text" className="form-control" ref="search_in" id="search_in" placeholder={ this.props.placeholder }/>
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
								<div className="row">
									<div className="col-sm-12">
										<span className="err-msg">{this.state.searchErrMsg}</span>
									</div>
								</div>
							</div>
						</div>
						{/* END row middle */}			
						{/* START row bottom */}

						<br/>


						{/*
						<div className="row bottom" id="bottom-header">
							<Route exact path="/" component={SearchSong}/>
							<Route path="/youtube" component={YoutubePlaylist}/>					
						</div>
						*/}

						{/* END row bottom */}
					</div>
				</div>
			
			</Router>

		);
	}
}

