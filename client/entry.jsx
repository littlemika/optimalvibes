import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';
import ReactDOM from 'react-dom';

import Header from './static/js/components/header.jsx';
import Body from './static/js/components/body.jsx';


export default class Base extends React.Component {
	render() {
		return(
			<div className="container-fluid">
				<Header/>
				<Body />
			</div>
		);
	}
}


var mount = document.getElementById('mount');
ReactDOM.render(<Base/>, mount);


	
		// 	<div>
		// 		<Header subtitle=daniel hui"/>
		// 		<Body />
		// 		<h1>{name} {this.getWorld()}</h1>
		// 	</div>
		// 