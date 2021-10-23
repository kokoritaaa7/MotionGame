using System.Runtime.InteropServices;
using TMPro;
using UnityEngine;
using RhythmGameStarter;

public class JSController : MonoBehaviour
{
    [DllImport("__Internal")]
    private static extern void _ResultSave(int score);

    public static void ResultSave(int score)
    {
#if !UNITY_EDITOR && UNITY_WEBGL
    _ResultSave(score);
#endif
    }

    [SerializeField]
    GameObject[] lineEffects;
    int maxLineNumber;
    int leftHandPos;
    int rightHandPos;
    bool isLeftKeyDown;
    bool isRightKeyDown;

    KeyboardInputHandler keyboardInputHandler;

    int testNum;

    // Start is called before the first frame update
    public void Start()
    {
        leftHandPos = 0;
        rightHandPos = 0;
        isLeftKeyDown = false;
        isRightKeyDown = false;
        maxLineNumber = lineEffects.Length;

        keyboardInputHandler = GetComponent<KeyboardInputHandler>();

        testNum = 0;
    }

    // Update is called once per frame
    public void Update()
    {
#if UNITY_EDITOR && USE_AUTOPLAY
        testNum++;

        if (testNum % 123 == 0)
        {
            leftHandPos = Random.Range(0, maxLineNumber + 1);
            rightHandPos = Random.Range(0, maxLineNumber + 1);
            //Debug.Log(" leftHandPos/rightHandPos" + leftHandPos + rightHandPos);
        }

        if(testNum % 5 == 0)
        {
            isLeftKeyDown = Random.Range(0, 2) == 0 ? true : false;
            isRightKeyDown = Random.Range(0, 2) == 0 ? true : false;
        }
#endif

        for (int i = 1; i <= maxLineNumber; i++)
        {
            if (i == leftHandPos)
            {
                lineEffects[i - 1].SetActive(true);
                keyboardInputHandler.isPressed[i - 1] = isLeftKeyDown;
            }
            else if (i == rightHandPos)
            {
                lineEffects[i - 1].SetActive(true);
                keyboardInputHandler.isPressed[i - 1] = isRightKeyDown;
            }
            else
            {
                lineEffects[i - 1].SetActive(false);
                keyboardInputHandler.isPressed[i - 1] = false;
            }
        }
    }

    public void UpdateLeftHandPos(int pos)
    {
        leftHandPos = pos;
    }

    public void UpdateRightHandPos(int pos)
    {
        rightHandPos = pos;
    }

    public void isLeftHandDown(int isDown)
    {
        isLeftKeyDown = isDown == 0 ? false : true;
    }

    public void isRightHandDown(int isDown)
    {
        isRightKeyDown = isDown == 0 ? false : true;
    }

    public void OnClickSaveScore()
    {
        int score = int.Parse(GameObject.Find("Score").GetComponent<TextMeshProUGUI>().text);
        Debug.Log("OnClickSaveScore > score : " + score);
        ResultSave(score);
    }
}