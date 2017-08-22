import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';
import TrackList from './track-list.jsx';


export default class Body extends React.Component {

	constructor(props) {
		super(props);
		
	}



	componentDidMount(){
	//	document.getElementById('#body').scrollTop += 20;
		var grabTrackURL = $('meta[name=grabTrackURL]').attr("content");
		var isDownloading = $('meta[name=isDownloading]').attr("content");
		console.log('get_data_url => ' +  grabTrackURL);
		console.log('isDownloading => ' + isDownloading);
	}

	render() {
		return (
			<div className="container" id="body">
			     {/* <Router>  */}
					<div className="row">
						<div className="col-sm-offset-2 col-sm-8">
							Loading right here
							<div id="loading">
							  	<br/><br/>
							  	<img src="/public/images/icons/loading-4.gif" className="center-content-h" alt="loading"/>
							  	<h4 className="center-content-h">Processing: Please Wait</h4>
							</div>
							 <a href="{{grab_track_url}}" id="download"  download>
                						<p>Download your tracks
                        						<button type="button" className="btn btn-default">
                                						<span class="glyphicon glyphicon-download-alt"></span>
                        						</button>
               							 </p>
        						</a>
	
	
						{/*
							<Route exact path="/" component={TrackList}/>
							<Route path="/spotify" component={TrackList}/>
							<Route path="/youtube" component={TrackList}/>
						*/}
						</div>
					</div>
			{/*	</Router>   */}
				
			</div>
		);
	}
}
