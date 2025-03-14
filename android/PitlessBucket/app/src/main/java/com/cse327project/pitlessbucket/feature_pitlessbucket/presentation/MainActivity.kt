package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.IntentSenderRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.toColorInt
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.cse327project.pitlessbucket.R
import com.cse327project.pitlessbucket.ui.theme.PitlessBucketTheme
import androidx.navigation.compose.rememberNavController
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.GoogleAuthUiClient
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.SignInScreen
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.SignInViewModel
import com.google.android.gms.auth.api.identity.Identity
import kotlinx.coroutines.launch

val fontFamily = FontFamily(
    Font(R.font.mplusrounded1c_thin, FontWeight.Thin),
    Font(R.font.mplusrounded1c_regular, FontWeight.Normal),
    Font(R.font.mplusrounded1c_medium, FontWeight.Medium),
    Font(R.font.mplusrounded1c_light, FontWeight.Light),
    Font(R.font.mplusrounded1c_extrabold, FontWeight.ExtraBold),
    Font(R.font.mplusrounded1c_bold, FontWeight.Bold),
    Font(R.font.mplusrounded1c_black, FontWeight.Black),

    )

class MainActivity : ComponentActivity() {

    private val googleAuthUiClient by lazy {
        GoogleAuthUiClient(
            context = applicationContext,
            oneTapClient = Identity.getSignInClient(applicationContext)
        )
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            PitlessBucketTheme {
//                DashboardLayout()
                Surface (
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    NavHost(navController=navController, startDestination = "sign_in") {
                        composable("sign_in"){
                            val viewModel = viewModel<SignInViewModel>()
                            val state by viewModel.state.collectAsStateWithLifecycle()

                            val launcher = rememberLauncherForActivityResult(
                                contract = ActivityResultContracts.StartIntentSenderForResult(),
                                onResult = { result ->
                                    if(result.resultCode == RESULT_OK) {
                                        lifecycleScope.launch {
                                            val signInResult = googleAuthUiClient.getSignInWithIntent(
                                                intent = result.data ?: return@launch
                                            )
                                            viewModel.onSignInResult(signInResult)
                                        }
                                    }
                                }
                            )

                            LaunchedEffect(key1= state.isSignInSuccessful) {
                                if(state.isSignInSuccessful){
                                    Toast.makeText(
                                        applicationContext,
                                        "Sign in successful",
                                        Toast.LENGTH_LONG
                                    ).show()
                                }
                            }

                            SignInScreen(
                                state=state,
                                onSignInClick = {
                                    lifecycleScope.launch {
                                        val signInIntentSender = googleAuthUiClient.signIn()
                                        launcher.launch(
                                            IntentSenderRequest.Builder(
                                                signInIntentSender ?:return@launch
                                            ).build()
                                        )
                                    }
                                }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DashboardLayout(modifier: Modifier = Modifier){
    Column {
        Box(
            modifier = modifier
                .fillMaxWidth()
                .fillMaxHeight(.11f)
                .background(Color("#3182ce".toColorInt()))
        ) {
            Row(
                modifier = modifier
                    .padding(top = 50.dp, start = 10.dp)
                    .fillMaxWidth()
            ) {
                Text(
                    text = "Pitless Bucket",
                    fontFamily = fontFamily,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color.White,
                    fontSize = 25.sp
                )
            }
        }
        Box(
            modifier = modifier
                .fillMaxWidth()
                .fillMaxHeight(.04f)
                .background(Color.White),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "Your Files & Folders",
                fontWeight = FontWeight.Bold,
                color = Color.Black,
                fontSize = 20.sp,
                textAlign = TextAlign.Center
            )
        }
    }
}



@Composable
fun SearchBarField(modifier: Modifier = Modifier){
    var text by remember {
        mutableStateOf(TextFieldValue(""))
    }


}

