import React from 'react';

const inject = params => UserComponent => props => (<UserComponent {...params} {...props}/>);

export default inject;