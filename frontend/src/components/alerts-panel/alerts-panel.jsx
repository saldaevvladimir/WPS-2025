import React, { forwardRef, useImperativeHandle } from 'react'
import './alerts-panel.css'

const AlertsPanel = forwardRef(({ autoDeleteTime }, ref) => {
	useImperativeHandle(ref, () => ({
		addAlert: (newAlert) => {
			const alertElement = document.createElement('div')
			alertElement.className = 'alert'
			alertElement.textContent = newAlert.message

			document.querySelector('.AlertsPanel').appendChild(alertElement)

			if (autoDeleteTime) {
				setTimeout(() => {
					alertElement.remove()
				}, autoDeleteTime * 1000)
			}
		}
	}))

	return (
		<div className='AlertsPanel'></div>
	)
})

export default AlertsPanel
