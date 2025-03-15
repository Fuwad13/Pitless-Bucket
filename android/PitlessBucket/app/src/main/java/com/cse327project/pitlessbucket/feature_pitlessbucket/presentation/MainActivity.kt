package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.IntentSenderRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.cse327project.pitlessbucket.R
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.ApiService
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.DashboardViewModel
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.DashboardViewModelFactory
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.components.DashboardScreen
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.file_upload.FileUploadViewModel
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.file_upload.FileUploadViewModelFactory
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.file_upload.components.FileUploadScreen
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.profile.ProfileScreen
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.GoogleAuthUiClient
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.SignInScreen
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.SignInViewModel
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.UserData
import com.cse327project.pitlessbucket.ui.theme.PitlessBucketTheme
import com.google.android.gms.auth.api.identity.Identity
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

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

    private val apiService: ApiService by lazy {
        val okHttpClient = OkHttpClient.Builder().build()
        val retrofit = Retrofit.Builder()
            .baseUrl("http://192.168.0.135:8000")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        retrofit.create(ApiService::class.java)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            PitlessBucketTheme {
                Surface (
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    NavHost(navController=navController, startDestination = "sign_in") {
                        composable("sign_in"){
                            val viewModel = viewModel<SignInViewModel>()
                            val state by viewModel.state.collectAsStateWithLifecycle()

                            LaunchedEffect(key1=Unit) {
                                if(googleAuthUiClient.getSignedInUser() != null){
                                    navController.navigate("dashboard")
                                }
                            }

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

                                    navController.navigate("dashboard")
                                    viewModel.resetState()
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
                        composable(route="profile") {
                            ProfileScreen(
                                userData = googleAuthUiClient.getGoogleIdToken(),
                                onSignOut = {
                                    lifecycleScope.launch {
                                        googleAuthUiClient.signOut()
                                        Toast.makeText(
                                            applicationContext,
                                            "Signed out",
                                            Toast.LENGTH_LONG
                                        ).show()

                                        navController.navigate("sign_in")
                                    }
                                }
                            )
                        }
                        composable("dashboard") {
                            val viewModel: DashboardViewModel = viewModel(
                                factory = DashboardViewModelFactory(apiService)
                            )

                            val userData = remember { mutableStateOf<UserData?>(null) }

                            LaunchedEffect(Unit) {
                                userData.value = googleAuthUiClient.getSignedInUser()
                                userData.value?.idToken?.let { idToken ->
                                    viewModel.setIdToken(idToken)
                                }
                            }
                            val state by viewModel.state.collectAsStateWithLifecycle()
                            DashboardScreen(userData = userData.value, state = state, navController=navController)
                        }
                        composable("file_upload") {
                            val viewModel: FileUploadViewModel = viewModel(
                                factory = FileUploadViewModelFactory(apiService)
                            )
                            val userData = remember { mutableStateOf<UserData?>(null) }
                            LaunchedEffect(Unit) {
                                userData.value = googleAuthUiClient.getSignedInUser()
                            }
                            val state by viewModel.state.collectAsStateWithLifecycle()
                            FileUploadScreen(userData = userData.value,state=state,navController=navController, viewModel = viewModel)
                        }


                    }
                }
            }
        }
    }
}



