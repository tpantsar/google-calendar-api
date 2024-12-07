import NotificationProps from '../types/NotificationProps'

const Notification = ({ message, type }: NotificationProps) => {
  if (message === null) {
    return null
  }

  if (type === 'error') {
    return <div className="notification notification-error">{message}</div>
  } else if (type === 'success') {
    return <div className="notification notification-success">{message}</div>
  } else {
    return <div className="notification notification-default">{message}</div>
  }
}

export default Notification
