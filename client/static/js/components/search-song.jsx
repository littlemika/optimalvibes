import React from 'react';
import SearchBar from './search-bar.jsx';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';




var DEFAULT_OPT_NAME = 'auto';


export default class SearchSong extends React.Component{

	constructor(props) {
		super(props);

		this.state = {
			selectedOption : DEFAULT_OPT_NAME
		}

		this.toggleOption = this.toggleOption.bind(this);
	}




	toggleOption(e) {
		this.setState({
			selectedOption : e.target.value
		});
	} 



	render() {
		return(
			<div>
			{/*
				<div className="col-sm-offset-3 col-sm-6">
					<p className="download-instructions center-content-h">
						Type in either <span className="highlight">(artist & song name)</span> or <span className="highlight">(youtube URL)</span>
					</p>
				</div>
			*/}
				<br/><br/><br/>
				<Router>
					<div className="col-sm-offset-3 col-sm-6" style={{fontSize: '.9em'}}>
						<div className="col-sm-6">
							{/* <div className="center-content-h" > */}
								{/*<label htmlFor="option">Filename Edit Options</label> */}
								<label id="filename-edit-options">Filename Edit Options:</label>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
								<select id="id3EditOptVal" value={this.state.selectedOption} onChange={this.toggleOption} name="option" className="selectpicker" >		
									<option value="auto">Auto</option>
									<option value="manual">Manual</option>
								</select>
							{/* </div> */}
						</div>
						<div className="col-sm-6 check-box-text">
							<p>{this.state.selectedOption=='auto' ? "This program will automatically edit your filename and metadata. Metadata is used by music players and software":
														  "You select the artist and title of the file and we'll do the rest"
								}
							</p>
						</div>
					</div>
				</Router>
			</div>
		);
	}
}