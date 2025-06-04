from  constants import L1,L2,L3,L4,L5,L6, STEPS, Q_ACTUAL
import numpy as np
from typing import Optional

class KInverse():
    def __init__ (self):
        self.q_actual = np.array(Q_ACTUAL)
        pass

    def rotx(self, theta):
        return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])

    def CINV6(self, pos):
        dk = L5 + L6
        R60 = self.rotx(np.pi)

        px = pos[0] - R60[0,2]*dk
        py = pos[1] - R60[1,2]*dk
        pz = pos[2] - R60[2,2]*dk

        D = (px**2 + py**2 + (pz - L1)**2 - L2**2 - (L3 + L4)**2) / (2 * L2 * (L3 + L4))
        if abs(D) > 1:
            raise ValueError('Punto inalcanzable')

        theta1 = np.arctan2(py, px)
        theta3 = np.arctan2(-np.sqrt(1 - D**2), D)
        theta2 = np.arctan2(pz - L1, np.sqrt(px**2 + py**2)) - np.arctan2((L3 + L4)*np.sin(theta3), L2 + (L3 + L4)*np.cos(theta3))

        q1, q2, q3 = theta1, theta2, -theta3

        R30 = np.array([
            [np.cos(q1+q2)*np.cos(q1), np.sin(q1), np.sin(q2+q3)*np.cos(q1)],
            [np.cos(q3+q2)*np.sin(q1), -np.cos(q1), np.sin(q2+q3)*np.sin(q1)],
            [np.sin(q2+q3), 0, -np.cos(q2+q3)]
        ])

        R63 = R30.T @ self.rotx(np.pi)

        theta5 = np.arctan2(np.sqrt(1 - R63[2,2]**2), R63[2,2]) - np.pi/2
        theta4 = np.arctan2(R63[1,2], R63[0,2])
        theta6 = np.arctan2(-R63[2,1], R63[2,0])

        if theta4 != 0:
            theta5 = np.pi + theta5

        return [q1, q2, q3, theta4, theta5 + np.pi, -theta6]


    def Inter(self, x: Optional[float] = 0, 
              y: Optional[float] = 0, 
              z: Optional[float] = 0):
            
        try: 
            p = [x,y,z]
            q = self.CINV6(p) 
            
            q_deg = [q[0]*180/np.pi] + [qi*180/np.pi for qi in q[1:]]
            q_deg = np.clip(np.round(q_deg), 0, 180)

            for s in range(1, STEPS + 1):
                q_interp = self.q_actual + (q_deg - self.q_actual) * (s / STEPS)
                q_interp = np.clip(np.round(q_interp), 0, 180)

                jsonData = {
                    's1': int(q_interp[0]),
                    's2': int(q_interp[1]),
                    's3': int(q_interp[2]),
                    's4': int(180 - q_interp[3] - 180),
                    's5': int(180 - q_interp[4]),
                    's6': int(q_interp[5])
                }

                print("→", jsonData)
                """requests.post(url, headers=headers, data=json.dumps(jsonData))
                time.sleep(pause_time) """
            self.q_actual = q_deg
            return jsonData

        except Exception as e: 
            print("Error: ", e)
        return 'na nai bo nai'

if __name__ == '__main__':
    intento = KInverse()
    intento.Inter(1,2,3)
