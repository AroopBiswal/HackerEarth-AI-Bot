import './pages/LandingPage.tsx'
import { Route, Routes } from 'react-router-dom'
import LandingPage from './pages/LandingPage.tsx'
import Chat from './pages/Chat.tsx'

function App() {

  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path='/chat' element={<Chat />} />
      </Routes>
    </>
  )
}

export default App
