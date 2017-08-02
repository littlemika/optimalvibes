import React from 'react';


/*
	Use:

	this.props{
		topic : topic,
		placeholder : placeholder,
		submit_text : submit_text
	}
		
*/
export default class SearchBar extends React.Component {

	render() {
		return(
			<searchbar>
				<div className="form-group">
					<label htmlFor="search_in">{ this.props.topic }</label>&nbsp;&nbsp;
					<input type="text" className="form-control" id="search_in" placeholder={ this.props.placeholder }/>
				</div>&nbsp;&nbsp;
				<button type="submit" className="btn btn-default btn-success">{ this.props.submit_text }</button>
			</searchbar>
		);
	}
}