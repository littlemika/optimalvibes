import React from 'react';


var tracks_json = [
	{
		'id': 1281723,
		'artist' : 'Kanye West',
		'track' : 'Slow Jamz',
		'length' : '4:37',
	},
	{
		'id': 982382,
		'artist' : 'Kishi Bashi',
		'track' : 'Windows',
		'length' : '3:39',
	},
	{
		'id': 29382891,
		'artist' : 'The Beatles',
		'track' : 'Blackbird',
		'length' : '2:20',
	}
];




class Track extends React.Component {
	render() {
		return(
	      <tr>
	        <td>{this.props.artist}</td>
	        <td>{this.props.track}</td>
	        <td>{this.props.length}</td>
	       {/* <td><input id={this.props.key} value="download" type="submit"/></td> */}
	        <td className="glyphicon-container"><span className="glyphicon glyphicon-download-alt" id={this.props.id}></span></td>
	      </tr>			    
		);
	}
}




export default class TrackList extends React.Component {

	render(){
		return(
			<tracklist>
				<table className="table borderless">
					<thead>
				      <tr>
				        <th>Artist</th>
				        <th>Track</th>
				        <th>Length</th>
				        <th>Download</th>
				      </tr>
				    </thead>
				    <tbody>
				    	{ 
				    		tracks_json.map(dict => {
				    			return <Track key={dict['id']} id={dict['id']} artist={dict['artist']}  track={dict['track']} length={dict['length']} />
				    	 	})
				    	}
				    </tbody>
				</table>
			</tracklist>
		);
	}
}